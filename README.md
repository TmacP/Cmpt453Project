There’s a number of different things you need to do to deal with text input:

    * Make sure you have added a text_trigger in your input_binding file 
        (default is input/game.input_binding).
    * Create a .gui and .gui_script with the text 
        nodes to use in your form
    * Detect using gui.pick_node() when the user clicks/taps the text nodes 
        and keep track of which text node you have selected.
    * Detect text input with the TEXT action_id 
        (unless you changed the action name in the input_binding file) in your 
        on_input() function. action.text will contain the pressed key.
    * Add the entered character to the text in the text node. 