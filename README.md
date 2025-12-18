# Pokemon Generation 3 Calculator

## https://feb-lon.github.io

This is a collection of Tools (with the most important ones being calculators) meant for Ironmon challenge runners. 
For information on what Ironmon is, visit https://gist.github.com/valiant-code/adb18d248fa0fae7da6b639e2ee8f9c1 and / or 
join the discord https://discord.gg/QEEsmNUX.

As Ironmon is a challenge that randomizes many aspects about the game, players have a hard time processing information 
via calculators meant for the original, un-randomized game. This page is my attempt to create a collection of tools 
to help Ironmon players.

## ATK / SPA Calculator

The biggest problem hereby (and also the biggest motivation for creating this page) is estimating the ATK / SPA of an 
opponent. 

## XP / EV Information

Gives information about the Yields from defeating a Pokemon, and can tell the XP difference between two levels.

## IV Calculator

When catching a new Pokemon, it can be quite useful to know how many IVs a Pokemon has. 
Adding EVs is planned.

## Technical Information

This calculator is written in Shiny for Python, converted to a static web application using Shinylive and deployed on 
Github Pages from the ``/docs`` directory.
To run it locally:

1. Clone the repo
2. install dependencies: ``shiny``, ``shinylive``, ``pandas``, ``numpy``
3. Run it via command ``shiny run calculator/app.py`` from the project directory
4. To create  the static page used in github pages, use ``shinylive export calculator docs``