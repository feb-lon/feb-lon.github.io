# Pokemon Generation 3 Calculator

## https://feb-lon.github.io

This is a collection of Tools (with the most important ones being calculators) meant for Ironmon challenge runners. 
For information on what Ironmon is, visit https://gist.github.com/valiant-code/adb18d248fa0fae7da6b639e2ee8f9c1 and / or 
join the discord https://discord.gg/QEEsmNUX.

As Ironmon is a challenge that randomizes many aspects about the game, players have a hard time processing information 
via calculators meant for the original, un-randomized game. This page is my attempt to create a collection of tools 
to help Ironmon players.

## ATK / SPA Calculator

This page is the main focus of this website.
It focuses on one of the biggest challenges in Ironmon:
Estimating the ATK / SPA of an opponent. 

This calculator was created and tested for use in generation 3, 
but changing the damage formula to later generations is possible. 
These however have less input options and were tested less.


## XP / EV Information

Contains Information about:
- The Yields from defeating a Pokemon, as well its weight and power for Low Kick
- How a stat would look like with a different nature
- XP difference between two levels
- How much confusion damage is to be expected

## IV Calculator

When catching a new Pokemon, it can be quite useful to know how many IVs a Pokemon has. 
This calculator currently ignores the topic of EVs completely, which depending on the use-case can be very impactful.

## Technical Information

This calculator is written in Shiny for Python, converted to a static web application using Shinylive and deployed on 
Github Pages from the ``/docs`` directory.
To run it locally:

1. Clone the repo
2. install dependencies: ``shiny``, ``shinylive``, ``pandas``, ``numpy``
3. Run it via command ``shiny run calculator/app.py`` from the project directory
4. To create  the static page used in github pages, use ``shinylive export calculator docs``