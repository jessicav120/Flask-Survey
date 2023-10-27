from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kikostinky'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    '''Starting page'''
    return render_template("home_page.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    '''Set session["responses"] to empty'''
    
    session["responses"] = []
    
    return redirect('/question/0')

@app.route("/question/<int:num>")
def question_page(num):
    '''Show current survey question.'''  
    responses = session.get("responses")
    
    #prevent skipping survey questions before completing
    if responses is None:
        return redirect("/")

    if num != len(responses):
        flash(f"Invalid question number: {num}")
        return redirect(f"/question/{len(responses)}")

    #show the question
    question = survey.questions[num]
    text = question.question
    choices = question.choices
    return render_template("question.html", text=text, choices=choices, title=survey.title)

@app.route("/answer", methods=["POST"])
def answer():
    '''Save answer to session["responses"] and redirect to next question'''
    
    #get answer from question form
    ans = request.form["ans"]
    
    #get session responses and append new answer to it
    responses = session["responses"]
    responses.append(ans)
    session["responses"] = responses
    
    #if all questions answered, thank the user
    if len(responses) == len(survey.questions):
        return redirect("/thank_you")
    #if not, continue to next question
    else: 
        return redirect(f"/question/{len(responses)}")

@app.route("/thank_you")
def thanks_page():
    '''Thank user for completing survey'''
    return render_template("thanks.html")
    