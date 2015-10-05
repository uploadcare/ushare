uShare
======


## Cheat sheet.

```term
git clone git@github.com:uploadcare/ushare.git
git remote set-url origin my_heroku_repo_url
git push origin master
```

## I don't want to deploy, I want to share!

### 1. Heroku.

Generally you can deploy [uShare](http://ushare.whitescape.com/) anywhere you like, but the fastest way is to use [heroku](http://www.heroku.com/).
First you'll need an account (it's free), heroku's [toolbelt](https://devcenter.heroku.com/articles/quickstart#step-2-install-the-heroku-toolbelt)
and some terminal-like stuff;

### 2. Create new app.

```term
heroku create my-ushare
```

### 3. Clone uShare

Get your copy of uShare repo and get in there:

```term
git clone git@github.com:uploadcare/ushare.git my-ushare
cd my-ushare
```

### 4. Set heroku as remote

Set your app's git repo URL (get it from [here](https://dashboard.heroku.com/apps) if you
missed it from step #1):

```term
git remote set-url origin git@heroku.com:my-ushare.git
```


### 5. Setup database

For Django applications, a Heroku Postgres database is automatically provisioned. This populates the `DATABASE_URL` environment variable.

Read more [about databse](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-the-add-on) and Heroku.


### 6. Install Uploadcare heroku add-on

```bash
heroku addons:add uploadcare
```

Read more bellow.


### 7. Finetuning

You may also want to set other system variables, like

- `DJANGO_DEBUG`
- `DJANGO_PRODUCTION_MODE`
- `DJANGO_SECRET_KEY`
- `UPLOADCARE_PUBLIC_KEY` - see bellow
- `UPLOADCARE_SECRET_KEY` - see bellow

### 8. Deploy!

```term
git push
```

## Heroku add-on

[Uploadcare add-on](https://addons.heroku.com/uploadcare/) for Heroku is in alpha stage,
so you may not be able to add it to your app. Contact hello@uploadcare.com to be invited to
be one of alpha users.


## Storage.

uShare uses [Uploadcare](https://uploadcare.com/) to store files — its demo-account by default:
all files are stored for one day, and **DELETED** after.
If you want a persistent storage, get the Uploadcare
[subscription](https://uploadcare.com/accounts/create/) and set obtained keys in
`ushare/settings/local.py` file:

```python
UPLOADCARE = {
    'pub_key': 'demopublickey',
    'secret': 'demoprivatekey',
}
```

Or you can set system variables:

```term
heroku config:set UPLOADCARE_PUBLIC_KEY='MY_PUBLIC_KEY'
heroku config:set UPLOADCARE_SECRET_KEY='MY_SECRET_KEY'
```

## Domain name.

Don't forget to set your domain name in django admin:
create a superuser (if you don't have one):

```term
heroku run python manage.py createsuperuser
```

login into django-admin (available at `/admin/` by default) and set the appropriate domain name to your Site-object.
