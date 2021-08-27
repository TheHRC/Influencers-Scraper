# Influencers-Scraper

Get's top 1000 Instagram influencer's list and scrapes their details as well as 5 recent post from Instagram along with Youtube subscribers &amp; Tiktok followers count.

## To get started

This project requires you have

- A [Hyperauditor](https://hypeauditor.com) account. [Signup Here](https://hypeauditor.com/signup/)

- An [Instagram](https://instagram.com) account.

## Install Python requirements

Use these commands

- Create, Activate a virtual environment and install requirements

- On mac & linux

```
    python3 -m venv env
    source ./env/Scripts/activate
    pip3 install requirements.txt
```

- On Windows

```
    python -m venv env
    env/Scripts/activate
    pip install
    requirements.txt
```

## Run the Project

- Follow the steps

```
    python get_influencers.py
```

> It will ask for the [Hyperauditor](https://hypeauditor.com) username and password

- Next

```
    python influencer.py
```

> It will ask for the [Hyperauditor](https://hypeauditor.com) username and password.
> and [Instagram](https://instagram.com) username and password.

This gets and creates an excel report of first 5 influencers.
You can change THE NUMBER in "line 197" as you want

## End Results

In the "Examples" folder, you can take a look of the end results of the scripts
- From "get_influencers.py"
> Influencer_data.txt

- From "influencer.py"
> cristiano.xlsx
