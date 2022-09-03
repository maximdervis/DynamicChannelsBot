from discord.ext import commands
import discord 
import asyncio

class Lobby:
	guild = None
	name = None 

	descriptionMsg = None

	category = None 
	voice_channel = None
	text_channel = None 

	owner = None

	def __init__(self, category, voice_channel, text_channel, owner):
		self.category = category 
		self.voice_channel = voice_channel 
		self.text_channel = text_channel
		self.owner = owner

	def __init__(self, guild, name):
		self.guild = guild
		self.name = name	

	async def set_users_limit(self, max_amnt):
		await self.voice_channel.edit(user_limit = int(max_amnt))

	async def set_description(self, description_text):
		if self.descriptionMsg == None :
			self.descriptionMsg = await self.text_channel.send(description_text) 
			await self.descriptionMsg.pin()
		else:
			await self.descriptionMsg.edit(content = description_text)


	async def change_name(self, name): 
		await self.voice_channel.edit(name = f'{name}-voice')
		await self.text_channel.edit(name = f'{name}-text')
		await self.category.edit(name = name)

	async def start_checking_empty(self, max_empty_state_time, checking_delay = 1):
		while len(self.voice_channel.members) != 0:
			await asyncio.sleep(checking_delay)
		await self.waitAndRemove(max_empty_state_time)

	async def setup_lobby(self):
			self.category = await self.guild.create_category (self.name)
			self.text_channel = await self.category.create_text_channel(self.name + '-text')
			self.voice_channel = await self.category.create_voice_channel(self.name + '-voice')

	async def remove(self):
		
		try:
			await self.category.delete() 
			await self.voice_channel.delete()
			await self.text_channel.delete()
		except:
			print('Object you\'r trying to delete has been removed')

	async def waitAndRemove(self, delay, checking_delay = 1):
		await asyncio.sleep(delay)
		try:
			if len(self.voice_channel.members) == 0:
				await self.remove()
			else:
				await self.start_checking_empty(delay, checking_delay)
			
		except:
			print('None variable access')  

