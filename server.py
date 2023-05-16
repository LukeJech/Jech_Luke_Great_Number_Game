from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = "There ain't no way you guess this key!"



@app.route('/')
def game_setup():
    too_high_low = ''
    reveal_answer = 'hidden'
    loss_screen = 'hidden'
    guess_active = 'block'
    #check to see if there has been a guess and if not don't display too high or too low if not
    if 'guess' not in session: 
        guess_response = 'hidden'  
        #setup a random answer in session
        session['answer'] = random.randint(1, 100)   
    else:
        guess_response = 'block'
        guess = int(session['guess'])
        answer = int(session['answer'])
        #check for 5 guesses
        if session['attempts'] >= 5 and guess != answer:
            too_high_low = ""
            guess_response = 'hidden'
            loss_screen = 'block'
            guess_active = 'hidden'
        #check if guess matches session answer and change page display based on guess
        if  guess > answer:
            too_high_low = "Too High!"
        elif  guess < answer:
            too_high_low = "Too Low!"
        else: 
            too_high_low = ""
            guess_response = 'hidden'
            reveal_answer = 'block'
            guess_active = 'hidden'
            

    return render_template("index.html", guess_response = guess_response, too_high_low = too_high_low, reveal_answer = reveal_answer, loss_screen = loss_screen, guess_active = guess_active )

@app.route('/guess', methods=['POST'])
def guess():
    #track amount of guesses
    if 'attempts' not in session: session['attempts'] = 1
    else: session['attempts'] += 1
    #set the session guess equal to num submited in form
    session['guess'] = request.form['guess']
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

@app.route('/leader', methods=['POST'])
def show_leaderboard():
    return render_template('leaderboard.html', first_name = request.form['first_name'], last_name = request.form['last_name'], attempts = session['attempts'] )


if __name__ == "__main__":
    app.run(debug = True)