from discord.ext import commands
import discord 
import asyncio

from lobby import Lobby

class LobbiesStorage:
	#stores lobby where channel takes place
	lobbies = {}

	def find_lobby_by_inner_id(self, inner_channel_id):
		return lobbies[voice_channel.id]

	def add_lobby(self, lobby):
		self.lobbies[lobby.voice_channel.id] = lobby
		self.lobbies[lobby.text_channel.id] = lobby

	def remove_lobby(self, lobby_to_rmv):
		for val, key in lobbies.items():
			if val == lobby_to_rmv:
				del lobbies[key]
				break

	def remove_lobby_by_id(self, lobby_id_to_rmv):
		del lobbies[lobby_id_to_rmv]



