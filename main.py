import tkinter as tk
import random
import time


# Define constants
BALL_SPEED = 5
PADDLE_SPEED = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20

# Initialize game variables
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED
paddle_dx = 0
ball_moving = False
score = 0

# Create the main window
window = tk.Tk()
window.title("Breakout Game")

# Create canvas for the game
canvas = tk.Canvas(window, width=400, height=400, bg="black")
canvas.pack()

# Create paddle
paddle = canvas.create_rectangle(150, 350, 250, 370, fill="white")

# Create ball
ball = canvas.create_oval(190, 190, 210, 210, fill="white")

# Create bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for row in range(5):
    for col in range(6):
        brick = canvas.create_rectangle(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50,
                                       (col + 1) * BRICK_WIDTH, (row + 1) * BRICK_HEIGHT + 50,
                                       fill=colors[row])
        bricks.append(brick)

# Function to move the paddle
def move_paddle(event):
    global paddle_dx
    paddle_dx = 0
    if event.keysym == "Left":
        paddle_dx = -PADDLE_SPEED
    elif event.keysym == "Right":
        paddle_dx = PADDLE_SPEED

# Function to start the game
def start_game(event):
    global ball_moving
    if not ball_moving:
        ball_moving = True
        move_ball()

# Function to move the ball
def move_ball():
    global ball_dx, ball_dy, ball_moving, score

    # Move the ball
    canvas.move(ball, ball_dx, ball_dy)
    
    # Check for collisions
    ball_pos = canvas.coords(ball)
    
    if ball_pos[2] >= 400 or ball_pos[0] <= 0:
        ball_dx = -ball_dx
    if ball_pos[1] <= 0:
        ball_dy = -ball_dy
    if ball_pos[3] >= 400:
        canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 24), fill="white")
        return
    
    # Check for collision with paddle
    if canvas.coords(ball)[2] >= canvas.coords(paddle)[0] and \
       canvas.coords(ball)[0] <= canvas.coords(paddle)[2] and \
       canvas.coords(ball)[3] >= canvas.coords(paddle)[1] and \
       canvas.coords(ball)[1] <= canvas.coords(paddle)[3]:
        ball_dy = -ball_dy
    
    # Check for collision with bricks
    for brick in bricks:
        if canvas.coords(ball)[2] >= canvas.coords(brick)[0] and \
           canvas.coords(ball)[0] <= canvas.coords(brick)[2] and \
           canvas.coords(ball)[3] >= canvas.coords(brick)[1] and \
           canvas.coords(ball)[1] <= canvas.coords(brick)[3]:
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 10
            break
    
    # Update score
    canvas.delete("score")
    canvas.create_text(50, 20, text=f"Score: {score}", font=("Helvetica", 14), fill="white", tags="score")
    
    # Move the paddle
    canvas.move(paddle, paddle_dx, 0)
    
    # Continue moving the ball
    if ball_moving:
        window.after(50, move_ball)

# Bind keys and start the game
window.bind("<Left>", move_paddle)
window.bind("<Right>", move_paddle)
window.bind("<space>", start_game)

# Start the game loop
window.mainloop()
