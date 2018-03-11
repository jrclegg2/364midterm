### Jack Clegg (jrclegg) - SI364 Midterm Project

This app allows 2 main features - one which allows you to search for a song and give it a rating, and see how close you are to the global rating that it has received. See how close you can get! The other feature allows you to search through the ratings in the database in 2 ways: By username, so you can see all of a user's ratings, or by song, so you can see all of a song's ratings.

API key can be reentered in the credentials.py file.

Route 1: '/' ---> 'songdata.html' or 'home.html'
Route 2: '/displayratings' ---> 'displayuserratings.html' or 'displaysongratings.html'
Route 3: '/searchratings' ---> 'allratings.html'

 ***Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)***
 App runs.

*** Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )***
 Navigation is seen on every page, pointing you to every page you could see.

 ***Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.***
 All templates inherit from base.html

 ***Include at least 2 additional template .html files we did not provide.***
 Included 5 - 'songdata.html', 'home.html', 'displayuserratings.html', 'displaysongratings.html', 'allratings.html'

 ***At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
These could be in the same template, and could be 1 of the 2 additional template files.***
Seen multiple places - ex: 'songdata.html' - for loop on lines 16 - 18, conditional on lines 10-12.

*** At least one errorhandler for a 404 error and a corresponding template.***
Can be found by going to any random link not defined above.

***At least one request to a REST API that is based on data submitted in a WTForm.***
API request to musixmatch.com on the '/' route, using the 'RatingForm' form.

*** At least one additional (not provided) WTForm that sends data with a GET request to a new page.***
Form is present on '/searchratings', and data is sent to '/displayratings'

 ***At least one additional (not provided) WTForm that sends data with a POST request to the same page.***
Form is present on '/', sends data to '/' as well.

 ***At least one custom validator for a field in a WTForm.***
Custom validator defined on lines 158 - 160

*** At least 2 additional model classes.***
3 additional model classes defined on lines 117 - 141

*** Have a one:many relationship that works properly built between 2 of your models.***
One user has multiple ratings.

 ***Successfully save data to each table.***
 Done in get_or_create functions, i.e in lines 190 (song), 191 (user), 192 (rating)

 ***Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).***
Ratings queried multiple times (i.e line 183), Song queried multiple times (i.e line 190), users queries (i.e line 191)

 ***Query data using an .all() method in at least one view function and send the results of that query to a template.***
 Queried ratings using .all() method on line 183, is shown in the 'songdata.html' template.

 ***Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)***
 Done multiple times, i.e line 228

*** Include at least one use of url_for. (HINT: This could happen where you render a form...)***
Done multiple times, i.e line 228

 ***Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)***
 home view function for route '/', display_ratings view function for '/displayratings', search_ratings for '/searchratings'


Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

***(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)***
Added model class for ratings, 3 columns present, save data in line 192, query data in line 183, data shown in 'songdata.html' on '/' route

***(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3)***
user is allowed to enter same song and new rating for it on '/' route, however this new data will not be saved
