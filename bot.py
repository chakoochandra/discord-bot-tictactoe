import os
import random

from discord.ext import commands
from dotenv import load_dotenv

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Tic
import tic

engine = create_engine("sqlite:///bot-tic.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, "tic"):
    Base.metadata.create_all(engine)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

description = "A simple tictactoe game"
bot = commands.Bot(command_prefix="?", description=description)


@bot.event
async def on_ready():
    print(bot.user.id, bot.user.name)


@bot.command(pass_context=True)
async def tic_ping(ctx):
    """Returns pong when called"""
    await ctx.send(
        "Hello for {} from {}, Let's play tictactoe!".format(
            ctx.message.author.name, ctx.message.guild.name
        )
    )


@bot.command(pass_context=True)
async def tic_clear(ctx):
    """Clear Game"""
    await ctx.send(clearGame(ctx))


def clearGame(ctx):
    author = ctx.message.author.name
    id = ctx.message.author.id

    try:
        modelTic = session.query(Tic).filter(Tic.id == id)
        if modelTic.first():
            modelTic.update({"history": []})
            session.commit()

        return "Previous game cleared. Let's play again, {}!".format(author)
    except Exception as e:
        return e


@bot.command(name="tic", help="Simple tictactoe game")
async def tic_start(ctx, no_of_cell: int = 0):
    await ctx.send(checkGame(ctx, no_of_cell))


def checkGame(ctx, no_of_cell):
    author = ctx.message.author.name
    avatar = str(ctx.message.author.avatar_url)
    id = ctx.message.author.id

    try:
        modelTic = session.query(Tic).filter(Tic.id == id)
        if not modelTic.first():
            state = tic.checkState([], no_of_cell)
            history = state["history"]
            session.add(Tic(id=id, name=author, avatar=avatar, history=history))
        else:
            state = tic.checkState(modelTic.first().history, no_of_cell)
            history = state["history"]
            modelTic.update({"history": history})

        # print("state", state)
        session.commit()

        board = "{} vs {} \n".format(bot.user.name, author) + state["board"]

        if state["status"] != None:
            board += state["status"].format(ctx.message.author.name)
            clearGame(ctx)
        else:
            board += "Your turn"

        return board
    except Exception as e:
        return e


bot.run(TOKEN)
