from XOGameObject import *  # Importing necessary classes and functions from XoGameObject.py

games = []  # List to hold all active games


# Function to get an existing game or create a new one
def get_game(game_id: str, player: dict = None) -> 'XOGame':
    """
    Retrieve an existing game or create a new one if it doesn't exist.
    :param game_id: The unique game ID.
    :param player: Player details if the game is newly created.
    :return: The game object.
    """
    for game in games:
        if game.game_id == game_id:
            return game
    games.append(XOGame(game_id, player))  # Create a new game if not found
    return games[-1]


# Function to remove a game by its ID
def remove_game(game_id: str) -> bool:
    """
    Removes a game from the list by its unique game ID.
    :param game_id: The unique game ID.
    :return: True if the game was removed, False otherwise.
    """
    for index in range(len(games)):
        if games[index].game_id == game_id:
            games.pop(index)  # Remove the game from the list
            return True
    return False


# Function to reset the game
def reset_game(game: 'XOGame') -> 'XOGame':
    """
    Rᴇsᴇᴛs ᴀɴ ᴇxɪsᴛɪɴɢ ɢᴀᴍᴇ ʙʏ ᴄʀᴇᴀᴛɪɴɢ ᴀ ɴᴇᴡ ᴏɴᴇ ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ᴘʟᴀʏᴇʀs.
    :param game: The game to reset.
    :return: A new game instance with the same players and game ID.
    """
    temp_game_id = game.game_id
    temp_p1 = game.player1  # Save player 1
    temp_p2 = game.player2  # Save player 2

    if remove_game(game.game_id):  # Remove the existing game
        games.append(XOGame(temp_game_id, temp_p1, temp_p2))  # Add a new game with same players
        return games[-1]  # Return the newly created game
    return None  # Return None if no game was reset
