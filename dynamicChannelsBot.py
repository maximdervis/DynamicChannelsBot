from discord.ext import commands
import discord 
import asyncio

import standard_messages 

from lobby import Lobby 
from storage import LobbiesStorage
import constants

client = commands.Bot(command_prefix = '!')
lobbies = LobbiesStorage()
					
#помощь по использованию бота
@client.command(name = 'помощь') 
async def help_bot(ctx):
	await ctx.send('Команды: ')
	await ctx.send(f'{client.command_prefix}лобби "имя лобби" "кол-во людей" "описание" - ручное создание лобби')
	await ctx.send(f'{client.command_prefix}префикс "символ" - изменение префикса для команд')

@client.command(name = 'запустить')
async def start_bot(ctx):
	pass 

#изменение префикса команд бота
@client.command(name = 'префикс')
async def change_prefix(ctx, new_prefix):
	if len(new_prefix) > 1:
		await ctx.send('Префикс должен состоять только из одного символа')
	elif len(new_prefix) == 1: 
		client.command_prefix = new_prefix
		await ctx.send('Префикс изменен')

@client.command(name = 'лобби')
async def create_lobby(ctx, lobby_name = 'новое-лобби', max_people_amnt = constants.DEFAULT_PEOPLE_AMNT, *, description = 'Обычное новое лобби'):
	if not correct_amnt(max_people_amnt):
		await ctx.send('Максимальное количество людей должно быть целым числом больше нуля') 
		return
	else:
		lobby = await instantiate_lobby(ctx.guild, lobby_name, max_people_amnt, description)
		
		await ctx.send(f'Лобби \'{lobby_name}\' было создано!')
		#перебрасываем того, кто создал лобби в него или просим зайти
		#если создатель не в гс 
		await process_lobby_creation(ctx.author, lobby) 
	
def correct_amnt(amnt):
	if not amnt.isdecimal():
		return False 
	elif int(amnt) < 1:
		return False
	else:
		return True 

@client.command(name = 'ограничение')
async def change_users_limit(ctx, new_users_limit):
	lobby = lobbies.lobbies[ctx.channel.id]
	if not correct_amnt(new_users_limit): 
		await ctx.send('Максимальное количество людей должно быть целым числом больше нуля')
	else:
		await lobby.set_users_limit(new_users_limit)
		await ctx.send(f'Установлено ограничение в {new_users_limit} пользователей')

@client.command(name = 'описание')
async def change_descriptin(ctx, *, new_description):
	lobby = lobbies.lobbies[ctx.channel.id]
	await lobby.set_description(new_description)

@client.command(name = 'название')
async def change_name(ctx, name):
	lobby = lobbies.lobbies[ctx.channel.id]
	await lobby.change_name(name)


async def process_lobby_creation (member, lobby): 
	await try_move_member_to_lobby(member, lobby)
	await lobby.start_checking_empty(constants.TIME_BEFORE_RMV_SEC, constants.EMPTY_CHECKING_DELAY_SEC)

async def try_move_member_to_lobby (member, lobby):
	if(member.voice != None): 
		await member.move_to(lobby.voice_channel)
		return True 
	else:
		return False

async def instantiate_lobby(guild, lobby_name, max_people_amnt, description):
	#создаем и устанавливаем параметры лобби
	lobby = Lobby(guild, lobby_name)
	await lobby.setup_lobby()

	await lobby.set_users_limit(max_people_amnt)

	#отправляем описание лобби в чат и закрепляем
	await lobby.set_description(description)

	lobbies.add_lobby(lobby)
	return lobby 

	
@client.event
async def on_voice_state_update(member, before, after):
	if not before.channel and after.channel:
		if after.channel.id == constants.LOBBY_CREATION_CHANNEL_ID: 
			description_of_room = f'Пустая комната пользователя {member.mention}'
			lobby = await instantiate_lobby (after.channel.guild, member.name, 10, description_of_room)
			await process_lobby_creation (member, lobby) 



client.run(constants.BOT_TOKEN)
creationLobbiesLobby = lobby()



