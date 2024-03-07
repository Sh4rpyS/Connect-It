09.03.2022: Changelog

    Optimizations:
    - Removed unneccessary collision drawing, improving performance by a lot

    Bug Fixes:
    - Fixed buttons being usable in different scenes
    - Fixed the border of the game being 1px off in both the x and y axis
    - Fixed tiles becoming displaced on higher level sizes
    - Fixed the DOTS being off positioned

    New Features:
    - Added text objects for Level, Level Pack and Level Size


12.03.2022: Changelog

    Optimizations:
    - Rewrote the highlighting code, making it faster and fixing
      problems that it had before

    New Features:
    - Added auto corner filling, so the line doesn't cut off so easily,
      also makes the game more playable on lower FPS
    - Added a launch option to remove Console
    - Added a launch option to change FPS lock
    - Added connecting lines between dots


13.03.2022: Changelog

    Optimizations:
    - Cleaned up the code (removed unneccessary/repeated code)
    - Optimized Levels menu to run a lot better, removed unneccessary
      updated

    Bug Fixes:
    - Fixed left alignment for the buttons has been fixed, others are still broken though
    - Fixed being able to cross wrong dots with lines

    New Features:
    - Added an icon for the game
    - Connected UI to level data
    - Added an ability to change text of the Text objects
    - Added a basic Level loading system
    - Added a basic level selection menu

  
14.03.2022: Changelog

    Optimizations:
    - Optimized buttons to improve performance when a lot of buttons are being drawn
    - Optimized ingame grid to have better performance with high huge levels


15.03.2022: Changelog

    Optimizations:
    - Optimized how borders are being drawn
    - Optimized how Tile alpha values are handled to improve performance
    - Fixed a performance issue when drawing Tiles
    
    Bug Fixes:
    - Fixed UI layering
    - Fixed loading a level in game changing editor level size
    - Fixed Tiles being 1px too big

    New Features:
    - Added input fields to the game
    - Added a new way to hide UI objects
    - New Level editor menu
    - New settings menu for editor
    - Level size option for level editor

    Other Changes:
    - Changed how level selection highlight looks


16.03.2022: Changelog

    Optimizations:
    - Optimized Tile updating even more

    Bug Fixes:
    - Fixed editor level size changing not working properly

    New Features:
    - Added level selection settings to the editor
    - Added pack name input field
    - Added a color picker
    - Dots can be placed in to the editor

    Other Changes:
    - Changed how the fade out time of the tiles
    - Moved load and save button position


17.03.2022: Changelog

    New Features:
    - Added a level completion indicator
    - Added text box to the editor
    - Added Saving and Loading
    - Added basic level advancing

    Other Changes:
    - Updated how the game UI looks
    - Changed the editor settings a little bit
    - Removed level names, levels now only have numbers

    Bug Fixes:
    - Fixed a random crash when switching progressing to a new level


18.03.2022: Changelog
    
    Bug Fixes:
    - Fixed a crash when resizing a level with dots
    - Fixed level completion not updating when advancing to the next level
    - Fixed a visual bug with color picker colors having black edges