# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

previous_move = "up"

def sortFoodByClosest(food, my_head):
    def sortFood(apple):
        xDiff = abs(apple["x"] - my_head["x"]);
        yDiff = abs(apple["y"] - my_head["y"]);
        return xDiff + yDiff
    foodSortedList = sorted(food, key=sortFood)
    return foodSortedList

def findClosestFoodFurtherFromOthers(snakes, foodSortedList, my_head):
    def callback(enemySnake):
        xDiff = abs(foodItem["x"] - my_head["x"]);
        yDiff = abs(foodItem["y"] - my_head["y"]);
        distanceFromMySnakeHead = xDiff + yDiff
        enemySnakeHead = enemySnake["body"][0]
        xDiff = abs(foodItem["x"] - enemySnakeHead["x"]);
        yDiff = abs(foodItem["y"] - enemySnakeHead["y"]);
        distanceFromEnemySnakeHead = xDiff + yDiff
        return distanceFromEnemySnakeHead >= distanceFromMySnakeHead

    closestFoodFurtherFromOthers = 0
    for foodItem in foodSortedList:
        allEnemySnakesAreFurther = all( callback(enemySnake) for enemySnake in snakes)
        if allEnemySnakesAreFurther:
            closestFoodFurtherFromOthers = foodItem
            break
    return closestFoodFurtherFromOthers

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START2")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER2\n")

    
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    global previous_move
    # global round
    # print("round: ", round)
    # round = round + 1
    return {"move": "left"}
    dangerous_health_state = 30
    search_for_food = False
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    
    if game_state["you"]["health"] < dangerous_health_state:
        search_for_food = True


    # if game_state["you"]["health"] < dangerous_health_state:
    #     search_for_food = True
     
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False


    occupied_boxes = []
    
    occupied_boxes = occupied_boxes.concatenate(game_state["you"]["body"])
    for snake in game_state["board"]["snakes"]:
        occupied_boxes = occupied_boxes.concatenate(snake["body"])
        
    

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']



    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}


    # if not search_for_food:
    print(f"MOVE {game_state['turn']}: Not need to search for food yet")
    if is_move_safe["left"] and previous_move == "up":
        print(f"MOVE {game_state['turn']}: Turning left")
        previous_move = "left"
        return {"move": "left"}
    if is_move_safe["down"] and previous_move == "left":
        print(f"MOVE {game_state['turn']}: Turning down")
        previous_move = "down"
        return {"move": "down"}
    if is_move_safe["right"] and previous_move == "down":
        print(f"MOVE {game_state['turn']}: Turning right")
        previous_move = "right"
        return {"move": "right"}
    if is_move_safe["up"] and previous_move != "right":
        print(f"MOVE {game_state['turn']}: Turning up")
        previous_move = "up"
        return {"move": "up"}
    
    # Choose a random move from the safse ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    foodSortedList = sortFoodByClosest(game_state['board']['food'], my_head)
    closestFoodFurtherFromOthers = findClosestFoodFurtherFromOthers(game_state["board"]["snakes"], foodSortedList, my_head)
    print(closestFoodFurtherFromOthers)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


def get_my_front_box(my_head, my_neck):
    front = 0
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        front = my_head
        front["x"] = front["x"] + 1
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        front = my_head
        front["x"] = front["x"] - 1
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        front = my_head
        front["y"] = front["y"] + 1
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        front = my_head
        front["y"] = front["y"] - 1
    return front
        
def get_my_left_box(my_head, my_neck):
    left = 0
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        left = my_head
        left["y"] = left["y"] + 1
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        left = my_head
        left["y"] = left["y"] - 1
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        left = my_head
        left["x"] = left["x"] - 1
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        left = my_head
        left["x"] = left["x"] + 1
    return left

def get_my_right_box(my_head, my_neck):
    right = 0
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        right = my_head
        right["y"] = right["y"] - 1
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        right = my_head
        right["y"] = right["y"] + 1
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        right = my_head
        right["x"] = right["x"] + 1
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        right = my_head
        right["x"] = right["x"] - 1
    return right


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
