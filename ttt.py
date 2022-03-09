import os, discord, random, pdb # pdb.set_trace()
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

gameOver = True
winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

@bot.command()
async def tictactoe(ctx, *, p2: discord.Member):
    global count
    global gameOver
    global player1
    global player2
    global board
    global temp_board
    global player_turn

    if not gameOver:
        await ctx.send("A game is already in progress, please finish it before starting a new one.")
        return
    else:
        player1 = ctx.author
        player2 = p2
        if ctx.author == p2:
            await ctx.send("Sorry, you cannot play with yourself.")
            return
        elif p2.bot:
            await ctx.send("Sorry, you cannot play with a bot.")
            return
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        makeBoard(board)
        await ctx.send(temp_board)
        gameOver = False # reset global vars
        count = 0
        player_num = random.randint(1, 2)
        if player_num == 1:
            player_turn = {ctx.author: ":regional_indicator_x:",}
            await ctx.send("<@" + str(ctx.author.id) + "> :regional_indicator_x: is first to play.")
        elif player_num == 2:
            player_turn = {p2: ":regional_indicator_x:"}
            await ctx.send("<@" + str(p2.id) + "> :regional_indicator_x: is first to play.")

@bot.command()
async def place(ctx, *, pos: int):
    # needed to bring in values from p1 and p2 in previous function
    global player1
    global player2
    # needed because these variables have their values changed (not only used)
    global count
    global gameOver
    global player_turn

    checkWinner(winningConditions) # various wrong input checks
    if gameOver:
        await ctx.send("There is no game in progress. Please use the **!tictactoe** command to start a new game.")
        return
    if ctx.author not in [player1, player2]:
        await ctx.send("You are not a player in the current game.")
        return
    if ctx.author != next(iter(player_turn)):
        await ctx.send("It is not your turn.")
        return
    if pos not in range(1,10):
        await ctx.send("Tile placements only allow numbers between 1 and 9 (inclusive).")
        return
    if board[pos-1] != ":white_large_square:":
        await ctx.send("Please choose an unmarked tile.")
        return
    
    if player1 in player_turn:
        board[pos-1] = player_turn[player1]
    else:
        board[pos-1] = player_turn[player2]

    makeBoard(board) # make board, print, change count
    await ctx.send(temp_board)
    count += 1

    checkWinner(winningConditions) # winning conditions check
    if gameOver == True:
        await ctx.send("<@" + str(ctx.author.id) + "> wins, congratulations! :tada:")
        return
    elif count == 9:
        gameOver = True
        await ctx.send("Tie game! :necktie:")
        return
    
    if player1 in player_turn:
        if player_turn[player1] == ":regional_indicator_x:":
            player_turn = {player2: ":o2:"}
        elif player_turn[player1] == ":o2:":
            player_turn = {player2: ":regional_indicator_x:"}
        await ctx.send("It is <@" + str(player2.id) + ">'s " + "(" + player_turn[player2] + ")" + " turn to play.")
    elif player2 in player_turn:
        if player_turn[player2] == ":regional_indicator_x:":
            player_turn = {player1: ":o2:"}
        elif player_turn[player2] == ":o2:":
            player_turn = {player1: ":regional_indicator_x:"}
        await ctx.send("It is <@" + str(player1.id) + ">'s " + "(" + player_turn[player1] + ")" + " turn to play.")

@bot.command()
async def quit(ctx):
    if ctx.author == player1 or ctx.author == player2:
        global board
        global gameOver
        global count
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        gameOver = True
        count = 0
        if ctx.author == player1:
            await ctx.send(ctx.author.name + " has quit. " + "<@" + str(player2.id) + "> wins by default. :rolling_eyes:")
        elif ctx.author == player2:
            await ctx.send(ctx.author.name + " has quit. " + "<@" + str(player1.id) + "> wins by default. :rolling_eyes:")
    else:
        await ctx.send("Sorry, you cannot quit a game if you are not a player.")

def makeBoard(board):
    global temp_board
    temp_board = ""
    for x in range(len(board)):
        if x == 2 or x == 5 or x == 8:
            temp_board += board[x] + "\n"
        else:
            temp_board += board[x] + " "

def checkWinner(winningConditions):
    global gameOver
    for tile in winningConditions:
        if (board[tile[0]] == ":regional_indicator_x:" and board[tile[1]] == ":regional_indicator_x:" and board[tile[2]] == ":regional_indicator_x:" 
        or board[tile[0]] == ":o2:" and board[tile[1]] == ":o2:" and board[tile[2]] == ":o2:"
        ):
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a player to play.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("That player does not exist. Please mention/ping a player (eg. **!tictactoe " + str(bot.user.name) + "** or **!tictactoe <@" + str(bot.user.id) + ">**).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("That position does not exist. Please make sure to enter an integer.")

bot.run(TOKEN)