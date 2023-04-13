import datetime
import random
import os
from googlesearch import search

from discord.ext import commands
from discord import Embed, Member, Intents, Colour

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN_SECRET")
    bot = commands.Bot(
        command_prefix=["m, ", "macaco, "],
        intents=Intents.all(),
        help_command=None
    )

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    @bot.command(
        brief="Retorna ping.",
        description="Retorna o ping do bot."
    )
    async def ping(ctx):
        embed = Embed(
            colour=Colour.green()
        )

        embed.add_field(
            name="",
            value="""
                Pong! 
                Latência: **{}ms**
            """.format(round(bot.latency * 1000)),
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(
        name="help",
        brief="Mostra os comandos do bot.",
        description="""
            `help`: Retorna todos os comandos do bot e uma descrição breve da cada um.
            `help [comando]`: Retorna a descrição de um comando em específico.
        """
    )
    async def bot_help(ctx, comm=None):
        if comm:
            embed = None

            for c in bot.walk_commands():
                if c.name == comm:
                    embed = Embed(
                        title="`{}`".format(c.name),
                        colour = Colour.yellow(),
                        timestamp = datetime.datetime.now(),
                    )

                    embed.add_field(
                        name="",
                        value="{}".format(c.description),
                        inline=False
                    )

                    break

            if embed is None:
                embed = Embed(
                    colour=Colour.red()
                )

                embed.add_field(
                    name="",
                    value="**:x: O comando informado não existe!**",
                    inline=False
                )

            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="{}, aqui está a lista de comandos: ".format(
                    ctx.author.nick if ctx.author.nick else ctx.author.name
                ),
                colour=Colour.yellow(),
            )

            comm_desc = ""

            for c in bot.walk_commands():
                comm_desc += "`{}` - {}\n".format(c.name, c.brief)

            embed.add_field(
                name="Comandos: ",
                value=comm_desc,
                inline=False
            )

            await ctx.send(embed=embed)

    @bot.command(
        name="userinfo",
        brief="Retorna informação de um usuário em específico.",
        description="""
            `userinfo`: Retorna as informações do próprio usuário.
            `userinfo @[nome/nick]`: Retorna as informações de um usuário em específico.
        """
    )
    async def user_info(ctx, member: Member = None):
        if member:
            target = member
        else:
            target = ctx.author

        embed = Embed(
            title="Informações de {}".format(target.name),
            colour=target.colour,
        )

        embed.set_thumbnail(url=target.avatar)
        embed.add_field(
            name="Nome: ",
            value=target.name,
            inline=False
        )
        embed.add_field(
            name="É um bot? ",
            value="Sim" if target.bot else "Não",
            inline=False
        )
        embed.add_field(
            name="Status: ",
            value=str(target.status).title() if str(target.status) != "dnd" else "Não pertube",
            inline=False
        )
        embed.add_field(
            name="Atividade: ",
            value="{} {}".format(
                str(target.activity.type).split(".")[-1].title(),
                target.activity.name
            ) if target.activity else "{} não está em nenhuma atividade no momento!".format(
                target.nick if target.nick else target.name
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(
        name="serverinfo",
        brief="Retorna informações sobre o server.",
        description="""
            `serverinfo`: Retorna as informações gerais do servidor em que o comando for usado.
        """
    )
    async def server_info(ctx):
        embed = Embed(
            title="Informação de {}".format(ctx.guild.name),
            colour=ctx.guild.owner.colour,
        )

        status = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))
        ]

        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(
            name="Criado em: ",
            value=ctx.guild.created_at.strftime("%d/%m/%Y"),
            inline=False
        )
        embed.add_field(
            name="Total de membros: ",
            value=len(ctx.guild.members),
            inline=False
        )
        embed.add_field(
            name="Total de humanos: ",
            value=len(list(filter(lambda m: not m.bot, ctx.guild.members))),
            inline=False
        )
        embed.add_field(
            name="Total de bots: ",
            value=len(list(filter(lambda m: m.bot, ctx.guild.members))),
            inline=False
        )
        embed.add_field(
            name="Status: ",
            value=""":green_circle: {} 
            
                  :yellow_circle: {} 
                  
                  :red_circle: {} 
                  
                  :black_circle: {}""".format(
                status[0],
                status[1],
                status[2],
                status[3]
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(
        name="members",
        brief="Retorna o número de membros no server.",
        description="""
            `members`: Retorna o número de membros no server (contando os bots).
        """
    )
    async def all_members(ctx):
        embed = Embed(
            colour=Colour.green()
        )

        embed.add_field(
            name="",
            value="O número de membros em {} é de: {}".format(ctx.guild.name, len(ctx.guild.members)),
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.command(
        name="search",
        brief="Procura e retorna links.",
        description="""
            `search [pesquisa]`: Retorna 5 links relacionados com a pesquisa.
            `search [pesquisa] [número de links]`: Retorna um número de links definido relacionados com a pesquisa.
            `search "[pesquisa]" [número de links]`: Caso sua pesquisa seja mais longa que uma palavra digite ela entre
            aspas.
        """
    )
    async def search_google(ctx, query, num_links=5):
        embed = Embed()

        if 20 >= num_links > 0:
            embed.title = "{}, aqui estão os links relacionados com '{}': ".format(
                ctx.author.nick if ctx.author.nick else ctx.author.name,
                query
            )
            embed.colour = Colour.green()

            links = [x for x in search(query, safe="on", num=num_links, stop=num_links)]

            for i, link in enumerate(links):
                embed.add_field(
                    name="**{}.** {}".format(i + 1, link),
                    value="",
                    inline=False
                )
        else:
            embed.colour = Colour.red()

            embed.add_field(
                name="",
                value="**:x: O número de links deve ser menor ou igual a 20 e maior que 0!**",
                inline=False
            )

        await ctx.send(embed=embed)

    @bot.command(
        brief="Retorna um número aleatório entre dois números.",
        description="""
            `roll`: Retorna um número aleatório entre 1 e 100.
            `roll [número limite]`: Retorna um número aleatório entre 1 e o número de escolha do usuário.
        """
    )
    async def roll(ctx, max_num=100):
        embed = Embed()

        if max_num > 1:
            embed.colour = Colour.green()

            embed.add_field(
                name="",
                value="Número escolhido: {}".format(random.randint(1, max_num + 1)),
                inline=False
            )
        else:
            embed.colour = Colour.red()

            embed.add_field(
                name="",
                value="**:x: O número máximo deve ser maior que 1!**",
                inline=False
            )

        await ctx.send(embed=embed)

    @bot.command(
        brief="Retorna uma escolha aleatória.",
        description="""
            `choose [elemento 1] [elemento 2] [elemento 3] ...`: Retorna um escolha aleatória entre N elementos.
        """
    )
    async def choose(ctx, *choices):
        embed = Embed(
            colour=Colour.green()
        )

        embed.add_field(
            name="",
            value="A minha escolha foi: **{}**".format(random.choice(choices)),
            inline=False
        )

        await ctx.send(embed=embed)

    bot.run(token)
