## Introduction and variables of game object
Hi, to explain how I made this project, I must start in the file game.py.
This is where I developed thewhole class for running a blackjack game. I
first started by making a list of 52 indices that would represent the 52
cards in a deck and a empty list that would later represent a shuffled deck.
In the function, shuffleDeck, I used a random number generator to choose a
card at random in the unshuffledDeck list to remove it from that list and
place it in the shuffledDeck list simulating a dealer in a casino shuffling
a deck. This method of using indices worked because I assigned each index to
represent a picture of a card in deckimg and represnt a value in deckValues.
Overall, this is how I simulated shuffling a deck. Next, with this shuffled
deck I could now start working on player and dealer hands. Since, in my game
I could only have two players, the dealer and the player, I elected to have
playerHand and dealerHand be within the game object (if I was expecting scalability,
i.e. multiple players with one dealer, I would have elected for creating separate
dealer and player objects). The playerhand and dealerHand both startedout empty
along with their respective cardimages and values being at 0. With these variables
created, I could start a game.
## calculatePlayerValue and calculateDealerValue functions
Before discussing, how the game works, I believe it is important to
discuss the calculatePlayerValue and calculateDealerValue functions.
Everytime, these functions are called it resets the numberOfAces within a
hand and its value. Now the reason why I put emphasis on the numberOfAces
is because an ace in blackjack can represent two numbers 1 or 11. Therefore,
it is important to know how many aces are in the hand. This is
because if the value goes over a certain number with a certain amount
of aces in the hand, we should count the aces with values of 1 instead of 11.
I implemented this for each instance according to each number of
aces a hand could have. I also sorted the deck to make sure that
we would not start counting the values ofthe aces until all of the cards that
only have one value (i.e. the rest of the cards in the deck that are not an ace)
had been counted. This feature was the same for each the player and the dealer.
Now, with that explained, I can start to talk about the other features
along with their implementation within in the app.
## logging into an account
I will start to talk about everything from the perspective of a user
going on the website. They will first be presented with a login screen
which will prompt them to input their username and password and then if
these inputs match with the username and password stored in the
database blackjack.db in table users, they will be logged in. On this
screen, they also have the option to reset password which will
replace their password in the database if they input the correct
username and password.
## Registering an account
If they do not have an account they can register which will input a new
username and password into the database. After this, they will be
sent to either two screens, the first being a screen that displays
"Play your first game" which will be rendered if there are no games
in the database for their userid. The other screen will render the last
ten games they have played along with the result of such game and the
money won/lost by queryring the game database for this information with
their userid. Once on this screen they have three options: play game,
add money, logout.
## Logout and addmoney options
The first one I will talk about is the logout button which will clear
the session and send them back to the login screen. Next we can talk
about add money which will send them to a screen where they can input
positive integer values and submit them to be added to their users cash
value. The app will take the input from this field and then update
the users cash value in the database to be the current value added
with the value in that input field.
## Playgame field along with explanation for using a global dictionary
Lastly, we can talk about the playgame field, this will ask the user
to input a positive integer value to wager in the game of blackjack.
Once inputted, and the play button is pressed, it will check the
database first to see if the user has enough money to wager, if not,
they will be sent to a screen saying that they do not have enough
money. If they do, a newgame object will be started and stored in a
global games dict with the key being their userid. This same method
will store their wager. I chose a global dictionary to allow me
to use this games object in routes/functions. Using this global
dictionary to store the wager and game allowed me to access them in
the gameO function, hit funciton, and resultOfGame function.
## Play game option and protocols for what happens when a new game is started
Moving on, with this startnewgame function, it will deal the cards
to both the player and dealer while storing their values and the
images of the cards. Then the app will immediately check for blackjack
by using the function in game.py which checks if the player's value
is equal to 21, since if the player has blackjack they automatically win, if there
is blackjack, it will render the result html and also update the
database to store the new game with all of its values such as money,
result, and userid which the userid will be used to access the values
money and result which are used in the index page. It will also update
the users cash value to be the current cash value plus double the wager
amount since it was blackjack(casinos usually have higher prizes
for blackjack). If there is no blackjack, it will render the gamehtml
which has two buttons hit and stand (corresponding to the options
in real blackjack).
## What happens when user presses hit
If the user presses hit, it will post to the hit page which will
acccess the newgame object and add a card to its hand, if they new
value is 21, it will automatically send it to the result page
for a runoff(which will be later discussed) since, you cannot get a
hand better than 21. It will then check for bust, which is checking
if the player value is over 21, if it is over 21, it will get the
result of the game ( a player loss since it is a bust ) and then it
make a variable loss, which is the negative value of the wager. Using
the same method as discussed for when it the user has blackjack, it
will update the game database and users cash amount. Then it will
render the result template. If the user has less than 21, it will
render the game template. Notice that while playerimg includes all
of the users card, while dealerimg only includes the first card and
then a "cover" card, this is because unless the game goes to a runoff
(which will be later discussed) the user can only see the dealers first
card. Cover is the backside of a card.
## What happens when users presses stand
Now, if the user presses stand, it will post to the /result route, this
will trigger a runoff, which is where the dealer will draw cards using
addDealerCard function until
they reach higher than 17 (following blackjack rules). Once it reaches
higher than 17, it will check the result of the game by comparing
variables playerValue and dealerValue. There are three
results, house wins(dealer wins) which will be if the dealersValue is
greater than playerValue, a push which is when both values are equal,
and a player win which is when the dealerValue is over 21 or the
playerValue is higher than the dealerValue. Again these will follow
the same method for updating the database with either adding 0,
-wagervalue, or the wagervalue depending on the result. It will then
render the result template with all the player cards and dealer cards
displayed along with the result. This template will also have a button
to go back to the home page.
## Final comments
That is it, this was blackjack. Some last comments, all features were
implemented to follow the basic rules of blackjack. Then I used a
template that follwed CS50's finance problem to keep the webpage
simplistic and also since the focus of this project was on working
the backend of a blackjack game. Last thing that I wanted to clarify
is that the css styling for displaying the cards was used to ensure
all cards could fit on the screen. Also, I used a jinja loop to display
all cards and assign them to their respective class. I used another
jinja loop for the index page which looped through a dictionary of
the game number, result, and money won/lost. With all being said,
this was blackjack, I hope you enjoy playing my game!



