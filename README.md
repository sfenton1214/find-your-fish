## Find Your Fish
### A CS50 Project by Skye Fenton and Dexter Summers, Fall 2018

The primary purpose of the available code is to make a website that functions as an interactive dichotomous key
for the freshwater fishes of Massachussets. That is, if you have a fish that you caught in the Charles, you could
pull up our website and through a series of questions discover what fish you had on your hands. This dichotomous key
is based off the one in "The Inland Fishes of Massachusetts", by David Halliwell, Alan Launer, and Harvard's own Karsten
Hartel.

In order to launch the website, execute flask run in the terminal while in the directory of the project codes.
Click on the provided link and you'll already be face to face with the first question. If your only goal is to
find out what your one fish is and get out, just start navigating through. Each question will ask if the fish's
physical characteristics fall into catagory A or B (e.g. (A) it has jaws (B) it doesn't). Click on the radio
button that corresponds to the correct catagory and click submit. This should take you to another question, or
possibly your fish. If it takes to another question, repeat the process. If it takes you to your fish, you should
be able to click on links that either search the Enyclopedia of Life for its entry on the fish or just generally
search Google Images so you can see if your fish resembles the one you've ended up at. There's also a link below
these that takes you back to the beginning (in case the button in the nav bar was just too far). You'll also
notice another card with a message telling you there's a feature there, but it's unavailable.

To gain access to this feature, you have to create an account by clicking the register tab in the nav bar, or
the log in tab if you've already created an account. These function as one would expect a log in or register
feature to. Once you're logged in, you'll have a new tab, "favorites." Going to this tab, on a new account, will
show an empty page. But, if you go to any fish page by navigating through the tree you'll now have the option to
favorite the fish. If this is done, you'll later be able to log in and look at your list of favorite fish. If
you want to go to that fish's page in order to get the link to Encyclopedia of Life or Google Images, you can
click on that fish and click on the submit button to go to its page.

Another feature that we made for this project was the checkcsv.py program. It is run in the terminal, taking a
command line argument of a csv. What this program does is it runs through a csv and makes sure that it correctly
constructs a dichotomous key. If it has anly flaws, it returns a list of rows with errors and what types of
errors they are so that the user can go back to their csv and fix it. This is an important part of the project
as it confirms that the hard-coded csv makes for an accurate website. If you want to test the code,
Findyourfish.csv should return no errors as it's what we use for the website and tester.csv is the same thing
but with a bunch of data randomly deleted from it, thus causing a bunch of errors.

Because of this, it's worth noting that while the layout of the html wouldn't make any sense, the code constitutes
a framework that anybody could utilize to make their own dichotomous key, provided they have the relevant csv
constructed.
