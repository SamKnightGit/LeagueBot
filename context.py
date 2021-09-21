from enum import Enum
from datetime import datetime
import response
import league
import parse_data

class Context(Enum):
    base = 0
    register_prompt = 1
    league_ign_prompt = 2
    league_ign_confirm = 3
    deregister_prompt = 4


class ContextManager:
    def __init__(self):
        self.user_contexts = {}
        self.games = {}

    def add_game(self, game_id):
        self.games[game_id] = datetime.now()

    def purge_games(self):
        now = datetime.now()
        for game_time in self.games.values():
            time_delta = now - game_time
            if time_delta.days > 0:
                del self.games[game_time]

    async def update_context(self, user_id, message):
        if context := self.user_contexts.get(user_id, None):
            await context.update(message)
        else:
            self.user_contexts[user_id] = await UserContext.create(message, user_id)


class UserContext:
    def __init__(self):
        self.user_id = None
        self.summoner_name = None
        self.account_id = None
        self.summoner_id = None
        self.is_registered = False
        self.context = Context.base

    @classmethod
    async def create(cls, message, user_id):
        self = UserContext()
        self.user_id = user_id
        self.summoner_name = None
        self.account_id = None
        self.summoner_id = None
        self.is_registered = False
        if message.content.lower() == "register":
            self.context = Context.league_ign_prompt
            await response.league_ign_prompt(message)
        else:
            self.context = Context.register_prompt
            await response.register_prompt(message)
        return self

    async def update(self, message):
        if self.context == Context.base:
            if self.is_registered:
                if message.content.lower() == "deregister":
                    self.context = Context.deregister_prompt
                    await response.deregister_prompt(message)
                else:
                    game_data = league.get_current_game(self.summoner_id)
                    if game_data is None:
                        await response.game_not_found(message)
                    else:
                        stats = await parse_data.parse_game_data(game_data, self.summoner_id)
                        await response.game_data(message, stats)
            else:
                self.context = Context.register_prompt
                await response.register_prompt(message)

        elif self.context == Context.register_prompt:
            if message.content.lower() in ['y', 'yes']:
                self.context = Context.league_ign_prompt
                await response.league_ign_prompt(message)

            else:
                self.context = Context.base
                await response.cancel_operation(message)

        elif self.context == Context.league_ign_prompt:
            result = league.get_summoner_by_name(message.content)
            if result is None:
                self.context = Context.base
                await response.league_ign_not_found(message)
            else:
                self.summoner_name = message.content.lower()
                self.summoner_id = result["id"]
                self.account_id = result["accountId"]
                self.context = Context.league_ign_confirm
                await response.league_ign_confirm(message)

        elif self.context == Context.league_ign_confirm:
            if message.content.lower() in ["y", "yes"]:
                self.is_registered = True
                self.context = Context.base
                await response.register_successful(message)
            else:
                self._reset()
                self.context = Context.base
                await response.cancel_operation(message)

        elif self.context == Context.deregister_prompt:
            if message.content.lower() in ["y", "yes"]:
                self._reset()
                self.context = Context.base
                await response.deregister_successful(message)
            else:
                self.context = Context.base
                await response.cancel_operation(message)

    def _reset(self):
        self.summoner_name = None
        self.summoner_id = None
        self.account_id = None
        self.is_registered = False
