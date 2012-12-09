uShare
============


## Cheat sheet.

<pre>
  <code>git clone git@heroku.com:ushare.git</code>
  <code>git remote set-url origin <i>my_heroku_repo_url</i></code>
  <code>git push origin master</code>
</pre>


## I don't want to deploy, I want to share!

1.
  Heroku. Generally you can deploy uShare anywhere you like, but the fastest way is to use
  [heroku](http://www.heroku.com/).
  First you'll need an account (it's free), heroku's
  [toolbelt](https://devcenter.heroku.com/articles/quickstart#step-2-install-the-heroku-toolbelt)
  and some terminal-like stuff;


2.
  Create an new app:
  <code>heroku create my-ushare</code>


3.
  Get your copy of uShare repo and get in there:
  <pre>
    <code>git clone git@heroku.com:ushare.git my-ushare</code>
    <code>cd my-ushare</code>
  </pre>


4.
  Set your app's git repo URL (get it from [here](https://dashboard.heroku.com/apps) if you missed it from step #1):
  <code>git remote set-url origin <i>git@heroku.com:my-ushare.git</i></code>


5.
  Create a database for your app:
  <code>heroku addons:add heroku-postgresql:dev</code>


6.
  Get the location of your database in:
  <code>heroku config</code>
  and set it as a default one:
  <code>heroku config:add DATABASE_URL=<i>my_database_url</i></code>


7.
  Push it!
  <code>git push</code>


## Storage.

uShare uses [Uploadcare](https://uploadcare.com/) to store files — its demo-account by default:
all files are stored for one day, and <strong>DELETED</strong> after.
If you want a persistent storage, get the Uploadcare
[subscription](https://uploadcare.com/accounts/create/) and set obtained keys in
<i>'ushare/settings/local.py'</i> file:

<pre>
  <code>UPLOADCARE = {</code>
  <code>    'pub_key': 'demopublickey',</code>
  <code>    'secret': 'demoprivatekey',</code>
  <code>}</code>
</pre>


## Static files.

Static is not collected by default — it's just dumped in a local folder, 'cause heroku wouldn't let things like
<code>python manage.py collectstatic</code>
You should use some external storages to handle this, like S3 or something else.
[Django-storages](http://django-storages.readthedocs.org/en/latest/index.html) may help you in that.


## Domain name.

Don't forget to set your domain name in django admin:
create a superuser (if you don't have one):
<code>heroku run python manage.py createsuperuser</code> 
login into django-admin ('<i>/admin/</i>' by default) and set the appropriate domain name to your Site-object.