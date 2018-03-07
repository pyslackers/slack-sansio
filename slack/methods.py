from enum import Enum

ROOT_URL = 'https://slack.com/api/'
HOOK_URL = 'https://hooks.slack.com'


class Methods(Enum):
    """
    Enumeration of available slack methods.

    Provides `iterkey` and `itermod` for :func:`SlackAPI.iter() <slack.io.abc.SlackAPI.iter>`.
    """
    # method = (ROOT_URL + method_url, iterkey, itermode, as_json)

    # api
    API_TEST = (ROOT_URL + 'api.test', None, None, True)

    # apps.permissions
    APPS_PERMISSIONS_INFO = (ROOT_URL + 'apps.permissions.info', None, None, False)
    APPS_PERMISSIONS_REQUEST = (ROOT_URL + 'apps.permissions.request', None, None, False)

    # auth
    AUTH_REVOKE = (ROOT_URL + 'auth.revoke', None, None, False)
    AUTH_TEST = (ROOT_URL + 'auth.test', None, None, True)

    # bots
    BOTS_INFO = (ROOT_URL + 'bots.info', None, None, False)

    # channels
    CHANNELS_ARCHIVE = (ROOT_URL + 'channels.archive', None, None, True)
    CHANNELS_CREATE = (ROOT_URL + 'channels.create', None, None, True)
    CHANNELS_HISTORY = (ROOT_URL + 'channels.history', 'timeline', 'messages', False)
    CHANNELS_INFO = (ROOT_URL + 'channels.info', None, None, False)
    CHANNELS_INVITE = (ROOT_URL + 'channels.invite', None, None, True)
    CHANNELS_JOIN = (ROOT_URL + 'channels.join', None, None, True)
    CHANNELS_KICK = (ROOT_URL + 'channels.kick', None, None, True)
    CHANNELS_LEAVE = (ROOT_URL + 'channels.leave', None, None, True)
    CHANNELS_LIST = (ROOT_URL + 'channels.list', 'cursor', 'channels', False)
    CHANNELS_MARK = (ROOT_URL + 'channels.mark', None, None, True)
    CHANNELS_RENAME = (ROOT_URL + 'channels.rename', None, None, True)
    CHANNELS_REPLIES = (ROOT_URL + 'channels.replies', None, None, False)
    CHANNELS_SET_PURPOSE = (ROOT_URL + 'channels.setPurpose', None, None, True)
    CHANNELS_SET_TOPIC = (ROOT_URL + 'channels.setTopic', None, None, True)
    CHANNELS_UNARCHIVE = (ROOT_URL + 'channels.unarchive', None, None, True)

    # chat
    CHAT_DELETE = (ROOT_URL + 'chat.delete', None, None, True)
    CHAT_ME_MESSAGE = (ROOT_URL + 'chat.meMessage', None, None, True)
    CHAT_POST_EPHEMERAL = (ROOT_URL + 'chat.postEphemeral', None, None, True)
    CHAT_POST_MESSAGE = (ROOT_URL + 'chat.postMessage', None, None, True)
    CHAT_UNFURL = (ROOT_URL + 'chat.unfurl', None, None, True)
    CHAT_UPDATE = (ROOT_URL + 'chat.update', None, None, True)

    # conversations
    CONVERSATIONS_ARCHIVE = (ROOT_URL + 'conversations.archive', None, None, True)
    CONVERSATIONS_CLOSE = (ROOT_URL + 'conversations.close', None, None, True)
    CONVERSATIONS_CREATE = (ROOT_URL + 'conversations.create', None, None, True)
    CONVERSATIONS_HISTORY = (ROOT_URL + 'conversations.history', 'cursor', 'messages', False)
    CONVERSATIONS_INFO = (ROOT_URL + 'conversations.info', None, None, False)
    CONVERSATIONS_INVITE = (ROOT_URL + 'conversations.invite', None, None, True)
    CONVERSATIONS_JOIN = (ROOT_URL + 'conversations.join', None, None, True)
    CONVERSATIONS_KICK = (ROOT_URL + 'conversations.kick', None, None, True)
    CONVERSATIONS_LEAVE = (ROOT_URL + 'conversations.leave', None, None, True)
    CONVERSATIONS_LIST = (ROOT_URL + 'conversations.list', 'cursor', 'channels', False)
    CONVERSATIONS_MEMBERS = (ROOT_URL + 'conversations.members', 'cursor', 'members', False)
    CONVERSATIONS_OPEN = (ROOT_URL + 'conversations.open', None, None, True)
    CONVERSATIONS_RENAME = (ROOT_URL + 'conversations.rename', None, None, True)
    CONVERSATIONS_REPLIES = (ROOT_URL + 'conversations.replies', 'cursor', 'messages', False)
    CONVERSATIONS_SET_PURPOSE = (ROOT_URL + 'conversations.setPurpose', None, None, True)
    CONVERSATIONS_SET_TOPIC = (ROOT_URL + 'conversations.setTopic', None, None, True)
    CONVERSATIONS_UNARCHIVE = (ROOT_URL + 'conversations.unarchive', None, None, True)

    # dialog
    DIALOG_OPEN = (ROOT_URL + 'dialog.open', None, None, True)

    # dnd
    DND_END_DND = (ROOT_URL + 'dnd.endDnd', None, None, True)
    DND_END_SNOOZE = (ROOT_URL + 'dnd.endSnooze', None, None, True)
    DND_INFO = (ROOT_URL + 'dnd.info', None, None, False)
    DND_SET_SNOOZE = (ROOT_URL + 'dnd.setSnooze', None, None, False)
    DND_TEAM_INFO = (ROOT_URL + 'dnd.teamInfo', None, None, False)

    # emoji
    EMOJI_LIST = (ROOT_URL + 'emoji.list', None, None, False)

    # files.comments
    FILES_COMMENTS_ADD = (ROOT_URL + 'files.comments.add', None, None, True)
    FILES_COMMENTS_DELETE = (ROOT_URL + 'files.comments.delete', None, None, True)
    FILES_COMMENTS_EDIT = (ROOT_URL + 'files.comments.edit', None, None, True)

    # files
    FILES_DELETE = (ROOT_URL + 'files.delete', None, None, True)
    FILES_INFO = (ROOT_URL + 'files.info', None, None, False)
    FILES_LIST = (ROOT_URL + 'files.list', 'page', 'files', False)
    FILES_REVOKE_PUBLIC_URL = (ROOT_URL + 'files.revokePublicURL', None, None, True)
    FILES_SHARED_PUBLIC_URL = (ROOT_URL + 'files.sharedPublicURL', None, None, True)
    FILES_UPLOAD = (ROOT_URL + 'files.upload', None, None, False)

    # groups
    GROUPS_ARCHIVE = (ROOT_URL + 'groups.archive', None, None, True)
    GROUPS_CLOSE = (ROOT_URL + 'groups.close', None, None, False)
    GROUPS_CREATE = (ROOT_URL + 'groups.create', None, None, True)
    GROUPS_CREATE_CHILD = (ROOT_URL + 'groups.createChild', None, None, False)
    GROUPS_HISTORY = (ROOT_URL + 'groups.history', 'timeline', 'messages', False)
    GROUPS_INFO = (ROOT_URL + 'groups.info', None, None, False)
    GROUPS_INVITE = (ROOT_URL + 'groups.invite', None, None, True)
    GROUPS_KICK = (ROOT_URL + 'groups.kick', None, None, True)
    GROUPS_LEAVE = (ROOT_URL + 'groups.leave', None, None, True)
    GROUPS_LIST = (ROOT_URL + 'groups.list', None, None, False)
    GROUPS_MARK = (ROOT_URL + 'groups.mark', None, None, True)
    GROUPS_OPEN = (ROOT_URL + 'groups.open', None, None, True)
    GROUPS_RENAME = (ROOT_URL + 'groups.rename', None, None, True)
    GROUPS_REPLIES = (ROOT_URL + 'groups.replies', None, None, False)
    GROUPS_SET_PURPOSE = (ROOT_URL + 'groups.setPurpose', None, None, True)
    GROUPS_SET_TOPIC = (ROOT_URL + 'groups.setTopic', None, None, True)
    GROUPS_UNARCHIVE = (ROOT_URL + 'groups.unarchive', None, None, True)

    # im
    IM_CLOSE = (ROOT_URL + 'im.close', None, None, True)
    IM_HISTORY = (ROOT_URL + 'im.history', 'timeline', 'messages', False)
    IM_LIST = (ROOT_URL + 'im.list', None, None, False)
    IM_MARK = (ROOT_URL + 'im.mark', None, None, True)
    IM_OPEN = (ROOT_URL + 'im.open', None, None, True)
    IM_REPLIES = (ROOT_URL + 'im.replies', None, None, False)

    # mpim
    MPIM_CLOSE = (ROOT_URL + 'mpim.close', None, None, True)
    MPIM_HISTORY = (ROOT_URL + 'mpim.history', 'timeline', 'messages', False)
    MPIM_LIST = (ROOT_URL + 'mpim.list', None, None, False)
    MPIM_MARK = (ROOT_URL + 'mpim.mark', None, None, True)
    MPIM_OPEN = (ROOT_URL + 'mpim.open', None, None, True)
    MPIM_REPLIES = (ROOT_URL + 'mpim.replies', None, None, False)

    # oauth
    OAUTH_ACCESS = (ROOT_URL + 'oauth.access', None, None, False)
    OAUTH_TOKEN = (ROOT_URL + 'oauth.token', None, None, False)

    # pins
    PINS_ADD = (ROOT_URL + 'pins.add', None, None, True)
    PINS_LIST = (ROOT_URL + 'pins.list', None, None, False)
    PINS_REMOVE = (ROOT_URL + 'pins.remove', None, None, True)

    # reactions
    REACTIONS_ADD = (ROOT_URL + 'reactions.add', None, None, True)
    REACTIONS_GET = (ROOT_URL + 'reactions.get', None, None, False)
    REACTIONS_LIST = (ROOT_URL + 'reactions.list', 'page', 'items', False)
    REACTIONS_REMOVE = (ROOT_URL + 'reactions.remove', None, None, True)

    # reminders
    REMINDERS_ADD = (ROOT_URL + 'reminders.add', None, None, True)
    REMINDERS_COMPLETE = (ROOT_URL + 'reminders.complete', None, None, True)
    REMINDERS_DELETE = (ROOT_URL + 'reminders.delete', None, None, True)
    REMINDERS_INFO = (ROOT_URL + 'reminders.info', None, None, False)
    REMINDERS_LIsT = (ROOT_URL + 'reminders.list', None, None, False)

    # rtm
    RTM_CONNECT = (ROOT_URL + 'rtm.connect', None, None, False)
    RTM_START = (ROOT_URL + 'rtm.start', None, None, False)

    # search
    SEARCH_ALL = (ROOT_URL + 'search.all', 'page', 'messages', False)
    SEARCH_FILES = (ROOT_URL + 'search.files', 'page', 'files', False)
    SEARCH_MESSAGES = (ROOT_URL + 'search.messages', 'page', 'messages', False)

    # starts
    STARS_ADD = (ROOT_URL + 'stars.add', None, None, True)
    STARS_LIST = (ROOT_URL + 'stars.list', 'page', 'items', False)
    STARS_REMOVE = (ROOT_URL + 'stars.remove', None, None, True)

    # team
    TEAM_ACCESS_LOGS = (ROOT_URL + 'teams.accessLogs', None, None, False)
    TEAM_BILLABLE_INFO = (ROOT_URL + 'teams.billableInfo', None, None, False)
    TEAM_INFO = (ROOT_URL + 'teams.info', None, None, False)
    TEAM_INTEGRATION_LOGS = (ROOT_URL + 'teams.integrationLogs', None, None, False)

    # team profile
    TEAM_PROFILE_GET = (ROOT_URL + 'teams.profile.get', None, None, False)

    # usergroups
    USERGROUPS_CREATE = (ROOT_URL + 'usergroups.create', None, None, True)
    USERGROUPS_DISABLE = (ROOT_URL + 'usergroups.disable', None, None, True)
    USERGROUPS_ENABLE = (ROOT_URL + 'usergroups.enable', None, None, True)
    USERGROUPS_LIST = (ROOT_URL + 'usergroups.list', None, None, False)
    USERGROUPS_UPDATE = (ROOT_URL + 'usergroups.update', None, None, True)

    # usergroups users
    USERGROUPS_USERS_LIST = (ROOT_URL + 'usergroups.users.list', None, None, False)
    USERGROUPS_USERS_UPDATE = (ROOT_URL + 'usergroups.users.update', None, None, True)

    # users
    USERS_DELETE_PHOTO = (ROOT_URL + 'users.deletePhoto', None, None, False)
    USERS_GET_PRESENCE = (ROOT_URL + 'users.getPresence', None, None, False)
    USERS_IDENTITY = (ROOT_URL + 'users.identity', None, None, False)
    USERS_INFO = (ROOT_URL + 'users.info', None, None, False)
    USERS_LIST = (ROOT_URL + 'users.list', 'cursor', 'members', False)
    USERS_SET_ACTIVE = (ROOT_URL + 'users.setActive', None, None, True)
    USERS_SET_PHOTO = (ROOT_URL + 'users.setPhoto', None, None, False)
    USERS_SET_PRESENCE = (ROOT_URL + 'users.setPresence', None, None, True)

    # users profile
    USERS_PROFILE_GET = (ROOT_URL + 'users.profile.get', None, None, False)
    USERS_PROFILE_SET = (ROOT_URL + 'users.profile.set', None, None, True)
