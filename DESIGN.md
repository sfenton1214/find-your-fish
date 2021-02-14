To start off, we adapted the flask and session configuration and layout code from the CS50 finanze problem set, as well as the
login_required and apology helper functions. We also took the register, check, and login functions that Skye had written for
her CS50 Finance.

The dichotomous key structure is a binary tree. We were originally going to give each node (a question or a fish
entry in the CSV) a unique tree id numbered in a way that the left branch of a node would always be a smaller number than the
parent node, and the right branch would always be a larger number than the parent node. Then we could create an algorithm
that moved down the tree based on this. We didn't end up doing this, as we realized that the tree ids would prevent the
tree's structure from being altered or added to if more fish were to be included, or if the species identification had to be
altered for some reason. Instead, we included in the csv an "a" and a "b" column for each entry that holds the csv id
of the next question or fish down the tree one the left or right branch. This didn't take up significantly more memory,
and it allows for the path from one node to the next to be easily altered.

We were originally going to use a csv of fish obtained from the MCZ, but it was more complicated than we needed it to be,
so we made one of our own including the fish and key questions. We decided to stay with using a hard coded csv as it is
easier for others to alter and add to than a SQL database, and the MCZ already uses them. The checkcsv.py program checks
to see if the csv has been altered incorrectly in a way that could lead to errors in the running of the website. It displays
how many errors are found in the csv (if nothing is pointing to the fish, if a question doesnt point to anything, etc), and
prints in the terminal the row number of the error. This allows users who alter the csv to easliy check their input.

We used SQL databases to keep track of the users registered, as we did in CS50 Finance, and used another SQL database to
keep track of users' favorited fish. The users database has columns for id, username, and the hash of their password, and
the favorites database has columns for id, user_id, and fishname. This allows for multiple users to favorite the same fish,
but still keeps their favorites distinct by user_id.

The 'index' page that the website first takes you to is the first question of the dichotomous key. This would be rendered with the "GET"
method. The "POST" method of the same get_index function is called when you submit subsequent "A" or "B" answers to questions.
This calls the same HTML question template but displays the next question whose id was stored in the "a" or "b" column in the
csv. It also checks if the next node down the tree is a fish by checking if it has a value for the "a" column; fish are the last
nodes in a tree branch so they do not connect to any other entry. If the next entry being called is a fish, the fish HTML page
is rendered displaying that specific fish.

We have made it so the key can be accessed without registering or logging in. But in order to favorite fish and keep a list of them,
the user must login. We made a variable called "verify" that is set to -1 "if not session", so if the user is not logged in. If
verify is -1, the fish HTML displays the message "If you were a logged in/registered user you could favorite this fish". If the
user is logged in, verify is set to the length of the SELECT return when selecting for the fishname in the favorites database where
the user id is equal to the current user's. This means that verify will equal 0 if this fish has not been inserted as this user's
favorite, and verify will equal 1 if this fish already has been inserted as a favorite. The fish HTML then displays the "Add to
favorites" button if verify is 0, or it displays the message "This is one of your favorite fish!" if verify is greater than 0. This
allows users who just have a passing fancy for the freshwater fish of New England to explore the key without registering, while
scientists and field workers can keep a record of found fish species. The verify variable also prevents a user from favoriting the
same fish more than once.

The fishinsert function is called when the user presses "Add to favorites" on the fish HTML. It retrieves the name of the fish from
the HTML page and inserts it into the favorites database with that user's id. It then redirects you to your favorites page. The
favorites page can also be reached through the navbar. The "GET" method of the favorites function retrieves all of the fish from the
favorites database with the current user's id and displays them with the favorites HTML. The "POST" method of favorites is called
when the user selects one of the favorite fish with a radio button and clicks the button "Go to Fish". This then renders the fish HTML
with that specific fish. The variable verify is set to equal 1 in this case as we know this fish has been favorited. The fish HTML also
has links to search for the fish in google images and the Encyclopedia of Life so you can check that the fish looks like your specimen
and to learn more about it.