from enum import Enum

ROOT_URL = 'https://slack.com/api/'
HOOK_URL = 'https://hooks.slack.com'


class Methods(Enum):
    """
    Enumeration of available slack methods.

    Provides `iterkey` and `itermod` for :func:`SlackAPI.iter() <slack.io.abc.SlackAPI.iter>`.
    """
    # api
    API_TEST = (ROOT_URL + 'api.test', None, None)

    # apps.permissions
    APPS_PERMISSIONS_INFO = (ROOT_URL + 'apps.permissions.info', None, None)
    APPS_PERMISSIONS_REQUEST = (ROOT_URL + 'apps.permissions.request', None, None)

    # auth
    AUTH_REVOKE = (ROOT_URL + 'auth.revoke', None, None)
    AUTH_TEST = (ROOT_URL + 'auth.test', None, None)

    # bots
    BOTS_INFO = (ROOT_URL + 'bots.info', None, None)

    # channels
    CHANNELS_ARCHIVE = (ROOT_URL + 'channels.archive', None, None)
    CHANNELS_CREATE = (ROOT_URL + 'channels.create', None, None)
    CHANNELS_HISTORY = (ROOT_URL + 'channels.history', 'timeline', 'messages')
    CHANNELS_INFO = (ROOT_URL + 'channels.info', None, None)
    CHANNELS_INVITE = (ROOT_URL + 'channels.invite', None, None)
    CHANNELS_JOIN = (ROOT_URL + 'channels.join', None, None)
    CHANNELS_KICK = (ROOT_URL + 'channels.kick', None, None)
    CHANNELS_LEAVE = (ROOT_URL + 'channels.leave', None, None)
    CHANNELS_LIST = (ROOT_URL + 'channels.list', 'cursor', 'channels')
    CHANNELS_MARK = (ROOT_URL + 'channels.mark', None, None)
    CHANNELS_RENAME = (ROOT_URL + 'channels.rename', None, None)
    CHANNELS_REPLIES = (ROOT_URL + 'channels.replies', None, None)
    CHANNELS_SET_PURPOSE = (ROOT_URL + 'channels.setPurpose', None, None)
    CHANNELS_SET_TOPIC = (ROOT_URL + 'channels.setTopic', None, None)
    CHANNELS_UNARCHIVE = (ROOT_URL + 'channels.unarchive', None, None)

    # chat
    CHAT_DELETE = (ROOT_URL + 'chat.delete', None, None)
    CHAT_ME_MESSAGE = (ROOT_URL + 'chat.meMessage', None, None)
    CHAT_POST_EPHEMERAL = (ROOT_URL + 'chat.postEphemeral', None, None)
    CHAT_POST_MESSAGE = (ROOT_URL + 'chat.postMessage', None, None)
    CHAT_UNFURL = (ROOT_URL + 'chat.unfurl', None, None)
    CHAT_UPDATE = (ROOT_URL + 'chat.update', None, None)

    # conversations
    CONVERSATIONS_ARCHIVE = (ROOT_URL + 'conversations.archive', None, None)
    CONVERSATIONS_CLOSE = (ROOT_URL + 'conversations.close', None, None)
    CONVERSATIONS_CREATE = (ROOT_URL + 'conversations.create', None, None)
    CONVERSATIONS_HISTORY = (ROOT_URL + 'conversations.history', 'cursor', 'messages')
    CONVERSATIONS_INFO = (ROOT_URL + 'conversations.info', None, None)
    CONVERSATIONS_INVITE = (ROOT_URL + 'conversations.invite', None, None)
    CONVERSATIONS_JOIN = (ROOT_URL + 'conversations.join', None, None)
    CONVERSATIONS_KICK = (ROOT_URL + 'conversations.kick', None, None)
    CONVERSATIONS_LEAVE = (ROOT_URL + 'conversations.leave', None, None)
    CONVERSATIONS_LIST = (ROOT_URL + 'conversations.list', 'cursor', 'channels')
    CONVERSATIONS_MEMBERS = (ROOT_URL + 'conversations.members', 'cursor', 'members')
    CONVERSATIONS_OPEN = (ROOT_URL + 'conversations.open', None, None)
    CONVERSATIONS_RENAME = (ROOT_URL + 'conversations.rename', None, None)
    CONVERSATIONS_REPLIES = (ROOT_URL + 'conversations.replies', 'cursor', 'messages')
    CONVERSATIONS_SET_PURPOSE = (ROOT_URL + 'conversations.setPurpose', None, None)
    CONVERSATIONS_SET_TOPIC = (ROOT_URL + 'conversations.setTopic', None, None)
    CONVERSATIONS_UNARCHIVE = (ROOT_URL + 'conversations.unarchive', None, None)

    # dialog
    DIALOG_OPEN = (ROOT_URL + 'dialog.open', None, None)

    # dnd
    DND_END_DND = (ROOT_URL + 'dnd.endDnd', None, None)
    DND_END_SNOOZE = (ROOT_URL + 'dnd.endSnooze', None, None)
    DND_INFO = (ROOT_URL + 'dnd.info', None, None)
    DND_SET_SNOOZE = (ROOT_URL + 'dnd.setSnooze', None, None)
    DND_TEAM_INFO = (ROOT_URL + 'dnd.teamInfo', None, None)

    # emoji
    EMOJI_LIST = (ROOT_URL + 'emoji.list', None, None)

    # files.comments
    FILES_COMMENTS_ADD = (ROOT_URL + 'files.comments.add', None, None)
    FILES_COMMENTS_DELETE = (ROOT_URL + 'files.comments.delete', None, None)
    FILES_COMMENTS_EDIT = (ROOT_URL + 'files.comments.edit', None, None)

    # files
    FILES_DELETE = (ROOT_URL + 'files.delete', None, None)
    FILES_INFO = (ROOT_URL + 'files.info', None, None)
    FILES_LIST = (ROOT_URL + 'files.list', 'page', 'files')
    FILES_REVOKE_PUBLIC_URL = (ROOT_URL + 'files.revokePublicURL', None, None)
    FILES_SHARED_PUBLIC_URL = (ROOT_URL + 'files.sharedPublicURL', None, None)
    FILES_UPLOAD = (ROOT_URL + 'files.upload', None, None)

    # groups
    GROUPS_ARCHIVE = (ROOT_URL + 'groups.archive', None, None)
    GROUPS_CLOSE = (ROOT_URL + 'groups.close', None, None)
    GROUPS_CREATE = (ROOT_URL + 'groups.create', None, None)
    GROUPS_CREATE_CHILD = (ROOT_URL + 'groups.createChild', None, None)
    GROUPS_HISTORY = (ROOT_URL + 'groups.history', 'timeline', 'messages')
    GROUPS_INFO = (ROOT_URL + 'groups.info', None, None)
    GROUPS_INVITE = (ROOT_URL + 'groups.invite', None, None)
    GROUPS_KICK = (ROOT_URL + 'groups.kick', None, None)
    GROUPS_LEAVE = (ROOT_URL + 'groups.leave', None, None)
    GROUPS_LIST = (ROOT_URL + 'groups.list', None, None)
    GROUPS_MARK = (ROOT_URL + 'groups.mark', None, None)
    GROUPS_OPEN = (ROOT_URL + 'groups.open', None, None)
    GROUPS_RENAME = (ROOT_URL + 'groups.rename', None, None)
    GROUPS_REPLIES = (ROOT_URL + 'groups.replies', None, None)
    GROUPS_SET_PURPOSE = (ROOT_URL + 'groups.setPurpose', None, None)
    GROUPS_SET_TOPIC = (ROOT_URL + 'groups.setTopic', None, None)
    GROUPS_UNARCHIVE = (ROOT_URL + 'groups.unarchive', None, None)

    # im
    IM_CLOSE = (ROOT_URL + 'im.close', None, None)
    IM_HISTORY = (ROOT_URL + 'im.history', 'timeline', 'messages')
    IM_LIST = (ROOT_URL + 'im.list', None, None)
    IM_MARK = (ROOT_URL + 'im.mark', None, None)
    IM_OPEN = (ROOT_URL + 'im.open', None, None)
    IM_REPLIES = (ROOT_URL + 'im.replies', None, None)

    # mpim
    MPIM_CLOSE = (ROOT_URL + 'mpim.close', None, None)
    MPIM_HISTORY = (ROOT_URL + 'mpim.history', 'timeline', 'messages')
    MPIM_LIST = (ROOT_URL + 'mpim.list', None, None)
    MPIM_MARK = (ROOT_URL + 'mpim.mark', None, None)
    MPIM_OPEN = (ROOT_URL + 'mpim.open', None, None)
    MPIM_REPLIES = (ROOT_URL + 'mpim.replies', None, None)

    # oauth
    OAUTH_ACCESS = (ROOT_URL + 'oauth.access', None, None)
    OAUTH_TOKEN = (ROOT_URL + 'oauth.token', None, None)

    # pins
    PINS_ADD = (ROOT_URL + 'pins.add', None, None)
    PINS_LIST = (ROOT_URL + 'pins.list', None, None)
    PINS_REMOVE = (ROOT_URL + 'pins.remove', None, None)

    # reactions
    REACTIONS_ADD = (ROOT_URL + 'reactions.add', None, None)
    REACTIONS_GET = (ROOT_URL + 'reactions.get', None, None)
    REACTIONS_LIST = (ROOT_URL + 'reactions.list', 'page', 'items')
    REACTIONS_REMOVE = (ROOT_URL + 'reactions.remove', None, None)

    # reminders
    REMINDERS_ADD = (ROOT_URL + 'reminders.add', None, None)
    REMINDERS_COMPLETE = (ROOT_URL + 'reminders.complete', None, None)
    REMINDERS_DELETE = (ROOT_URL + 'reminders.delete', None, None)
    REMINDERS_INFO = (ROOT_URL + 'reminders.info', None, None)
    REMINDERS_LIsT = (ROOT_URL + 'reminders.list', None, None)

    # rtm
    RTM_CONNECT = (ROOT_URL + 'rtm.connect', None, None)
    RTM_START = (ROOT_URL + 'rtm.start', None, None)

    # search
    SEARCH_ALL = (ROOT_URL + 'search.all', 'page', 'messages')
    SEARCH_FILES = (ROOT_URL + 'search.files', 'page', 'files')
    SEARCH_MESSAGES = (ROOT_URL + 'search.messages', 'page', 'messages')

    # starts
    STARS_ADD = (ROOT_URL + 'stars.add', None, None)
    STARS_LIST = (ROOT_URL + 'stars.list', 'page', 'items')
    STARS_REMOVE = (ROOT_URL + 'stars.remove', None, None)

    # team
    TEAM_ACCESS_LOGS = (ROOT_URL + 'teams.accessLogs', None, None)
    TEAM_BILLABLE_INFO = (ROOT_URL + 'teams.billableInfo', None, None)
    TEAM_INFO = (ROOT_URL + 'teams.info', None, None)
    TEAM_INTEGRATION_LOGS = (ROOT_URL + 'teams.integrationLogs', None, None)

    # team profile
    TEAM_PROFILE_GET = (ROOT_URL + 'teams.profile.get', None, None)

    # usergroups
    USERGROUPS_CREATE = (ROOT_URL + 'usergroups.create', None, None)
    USERGROUPS_DISABLE = (ROOT_URL + 'usergroups.disable', None, None)
    USERGROUPS_ENABLE = (ROOT_URL + 'usergroups.enable', None, None)
    USERGROUPS_LIST = (ROOT_URL + 'usergroups.list', None, None)
    USERGROUPS_UPDATE = (ROOT_URL + 'usergroups.update', None, None)

    # usergroups users
    USERGROUPS_USERS_LIST = (ROOT_URL + 'usergroups.users.list', None, None)
    USERGROUPS_USERS_UPDATE = (ROOT_URL + 'usergroups.users.update', None, None)

    # users
    USERS_DELETE_PHOTO = (ROOT_URL + 'users.deletePhoto', None, None)
    USERS_GET_PRESENCE = (ROOT_URL + 'users.getPresence', None, None)
    USERS_IDENTITY = (ROOT_URL + 'users.identity', None, None)
    USERS_INFO = (ROOT_URL + 'users.info', None, None)
    USERS_LIST = (ROOT_URL + 'users.list', 'cursor', 'members')
    USERS_SET_ACTIVE = (ROOT_URL + 'users.setActive', None, None)
    USERS_SET_PHOTO = (ROOT_URL + 'users.setPhoto', None, None)
    USERS_SET_PRESENCE = (ROOT_URL + 'users.setPresence', None, None)

    # users profile
    USERS_PROFILE_GET = (ROOT_URL + 'users.profile.get', None, None)
    USERS_PROFILE_SET = (ROOT_URL + 'users.profile.set', None, None)
