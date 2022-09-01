# Jaguar Run 
Final project for Harvard's edX CS50P ending Dec. 30, 2022. Simpel side scrolling video game made wioth pygame. 

#### Video Demo: <URL_HERE>

## Description:
Ancient Mayan themed side-scrolling video game where you try to survive as long as possible by jumping over, crouching under, and/or attacking enemies.

<b>Jaguar Run</b> is a simple python game we created using ```pygame```. 

We orgnized the project into the following files:
- ```project.py``` - the main python file you need to execute to run the game.
- ```game.py``` - contains the 'Game' class which is responsible for composing all of the various elements into a cohesive application. This includes: the intro screen, user input handling, background animation, collision detection, and game persistence.
- ```player.py``` - contains the 'Player' class which is responsible for encapsulating all of the player-related attributes and logic. This includes: images/sprites, sound effects, and animations.
- ```enemy.py``` - contains the 'Enemy' class which is responsible for encapsulating all of the enemy-related attributes and logic. This includes: images/sprites, sound effects, and animations. 
- ```config.py``` - contains all of the game constants, such as: gravity, ground height, screen size, player speed, etc.
- ```test_project.py``` - contains all of the tests for verifying things are working as expected.
- ```README.md``` - This file!
- ```requirements.txt``` - The list of 3rd party libraries needed to be installed via pip.

## Project Concept ##
We brainstormed many different ideas for the final project before settling on a game. Initially we wanted to try creating a pytorch ML classifier (i.e. not a hotdog :), but then we stunmbled upon pygame and decided we needed to make a game.

We narrowed it down to either a Tower Defense game, a Zelda-style RPG, or a side-scroller. Our ultimate vision is to create a hybrid Zelda-style RPG, where the main character roams a map to access the various levels, and the levels themselves include a mix of zelda-style, side-scrolling, and tower defense "mini-games".

We quickly realized the scope of our vision was much too large for the final project, so we narrowed it down to a single side-scrolling example level: Jaguar Run.

## Game Assets ##
We utlilized [midjourney](https://www.midjourney.com/home/) & [Dall-E 2](https://openai.com/dall-e-2/) to help generate the visual assets used in the game. For instance, the main player character was generated via Dall-E 2 using the prompt: ```Ancient Mayan Jaguar Chaac God 16-bit style```. 

Using Gimp, we then manually created all of the character image variations including: stand, walk, crouch, jump, walk-attack, jump-attack, and just for fun, crouch-attack :)

The background layers/assets were purchased from here:<br> https://gameartpartners.com/downloads/mayan-temple-game-background/

Music and sound effects were obtained from various free gaming content websites, such as: freesound.org, pixabay.com, and chosic.com.

[See asset attributions below](#ca).

## Background Animation ##
The intro screen background was generated via Midjourney.

We discussed several ideas for the game background while playing, including additional A.I. generated art, but after finding the background assets linked to above, we decided we decided to go with a parallax scrolling background because the assets looked great, fit our needs, and because we've always wanted to learn how to do parallax scrolling. This was very satisfying to implement and to see working!

## Gameplay ##
The game started out as a simple "flappy-bird"-style game where you just jump over enemies. However, we added additional gameplay functionality to make the game more fun. This included the ability to move forwards & backwards, crouching, and attacking. We also added attack effects, sounds, high score, game persitence, and various other little things like the "konomi code" on the main intro screen :)

### Controls ###
- Jump - ```UP```
- Crouch - ```DOWN```
- Forward - ```RIGHT```
- Backward - ```LEFT```
- Attack - ```SPACE```
- Save & Exit - ```ESCAPE``` (during gameplay only)

## Installation ##

## Asset Attibution...
<a name="ca"></a>
- [Background Track](audio/legend-of-narmer.mp3):  
The Legend of Narmer by WombatNoisesAudio | https://soundcloud.com/user-734462061
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/
Music promoted by https://www.chosic.com/free-music/all/
