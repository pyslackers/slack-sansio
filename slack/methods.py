from enum import Enum
from collections import namedtuple

ROOT_URL: str = "https://slack.com/api/"
HOOK_URL: str = "https://hooks.slack.com"
method = namedtuple("method", ("url", "itermode", "iterkey", "as_json"))


class Methods(Enum):
    """
    Enumeration of available slack methods.

    Provides `iterkey` and `itermod` for :func:`SlackAPI.iter() <slack.io.abc.SlackAPI.iter>`.
    """

    # api
    API_TEST = method(ROOT_URL + "api.test", None, None, True)

    # apps.permissions
    APPS_PERMISSIONS_INFO = method(
        ROOT_URL + "apps.permissions.info", None, None, False
    )
    APPS_PERMISSIONS_REQUEST = method(
        ROOT_URL + "apps.permissions.request", None, None, False
    )

    # auth
    AUTH_REVOKE = method(ROOT_URL + "auth.revoke", None, None, False)
    AUTH_TEST = method(ROOT_URL + "auth.test", None, None, True)

    # bots
    BOTS_INFO = method(ROOT_URL + "bots.info", None, None, False)

    # channels
    CHANNELS_ARCHIVE = method(ROOT_URL + "channels.archive", None, None, True)
    CHANNELS_CREATE = method(ROOT_URL + "channels.create", None, None, True)
    CHANNELS_HISTORY = method(
        ROOT_URL + "channels.history", "timeline", "messages", False
    )
    CHANNELS_INFO = method(ROOT_URL + "channels.info", None, None, False)
    CHANNELS_INVITE = method(ROOT_URL + "channels.invite", None, None, True)
    CHANNELS_JOIN = method(ROOT_URL + "channels.join", None, None, True)
    CHANNELS_KICK = method(ROOT_URL + "channels.kick", None, None, True)
    CHANNELS_LEAVE = method(ROOT_URL + "channels.leave", None, None, True)
    CHANNELS_LIST = method(ROOT_URL + "channels.list", "cursor", "channels", False)
    CHANNELS_MARK = method(ROOT_URL + "channels.mark", None, None, True)
    CHANNELS_RENAME = method(ROOT_URL + "channels.rename", None, None, True)
    CHANNELS_REPLIES = method(ROOT_URL + "channels.replies", None, None, False)
    CHANNELS_SET_PURPOSE = method(ROOT_URL + "channels.setPurpose", None, None, True)
    CHANNELS_SET_TOPIC = method(ROOT_URL + "channels.setTopic", None, None, True)
    CHANNELS_UNARCHIVE = method(ROOT_URL + "channels.unarchive", None, None, True)

    # chat
    CHAT_DELETE = method(ROOT_URL + "chat.delete", None, None, True)
    CHAT_GET_PERMALINK = method(ROOT_URL + "chat.getPermalink", None, None, False)
    CHAT_ME_MESSAGE = method(ROOT_URL + "chat.meMessage", None, None, True)
    CHAT_POST_EPHEMERAL = method(ROOT_URL + "chat.postEphemeral", None, None, True)
    CHAT_POST_MESSAGE = method(ROOT_URL + "chat.postMessage", None, None, True)
    CHAT_UNFURL = method(ROOT_URL + "chat.unfurl", None, None, True)
    CHAT_UPDATE = method(ROOT_URL + "chat.update", None, None, True)

    # conversations
    CONVERSATIONS_ARCHIVE = method(ROOT_URL + "conversations.archive", None, None, True)
    CONVERSATIONS_CLOSE = method(ROOT_URL + "conversations.close", None, None, True)
    CONVERSATIONS_CREATE = method(ROOT_URL + "conversations.create", None, None, True)
    CONVERSATIONS_HISTORY = method(
        ROOT_URL + "conversations.history", "cursor", "messages", False
    )
    CONVERSATIONS_INFO = method(ROOT_URL + "conversations.info", None, None, False)
    CONVERSATIONS_INVITE = method(ROOT_URL + "conversations.invite", None, None, True)
    CONVERSATIONS_JOIN = method(ROOT_URL + "conversations.join", None, None, True)
    CONVERSATIONS_KICK = method(ROOT_URL + "conversations.kick", None, None, True)
    CONVERSATIONS_LEAVE = method(ROOT_URL + "conversations.leave", None, None, True)
    CONVERSATIONS_LIST = method(
        ROOT_URL + "conversations.list", "cursor", "channels", False
    )
    CONVERSATIONS_MEMBERS = method(
        ROOT_URL + "conversations.members", "cursor", "members", False
    )
    CONVERSATIONS_OPEN = method(ROOT_URL + "conversations.open", None, None, True)
    CONVERSATIONS_RENAME = method(ROOT_URL + "conversations.rename", None, None, True)
    CONVERSATIONS_REPLIES = method(
        ROOT_URL + "conversations.replies", "cursor", "messages", False
    )
    CONVERSATIONS_SET_PURPOSE = method(
        ROOT_URL + "conversations.setPurpose", None, None, True
    )
    CONVERSATIONS_SET_TOPIC = method(
        ROOT_URL + "conversations.setTopic", None, None, True
    )
    CONVERSATIONS_UNARCHIVE = method(
        ROOT_URL + "conversations.unarchive", None, None, True
    )

    # dialog
    DIALOG_OPEN = method(ROOT_URL + "dialog.open", None, None, True)

    # dnd
    DND_END_DND = method(ROOT_URL + "dnd.endDnd", None, None, True)
    DND_END_SNOOZE = method(ROOT_URL + "dnd.endSnooze", None, None, True)
    DND_INFO = method(ROOT_URL + "dnd.info", None, None, False)
    DND_SET_SNOOZE = method(ROOT_URL + "dnd.setSnooze", None, None, False)
    DND_TEAM_INFO = method(ROOT_URL + "dnd.teamInfo", None, None, False)

    # emoji
    EMOJI_LIST = method(ROOT_URL + "emoji.list", None, None, False)

    # files.comments
    FILES_COMMENTS_ADD = method(ROOT_URL + "files.comments.add", None, None, True)
    FILES_COMMENTS_DELETE = method(ROOT_URL + "files.comments.delete", None, None, True)
    FILES_COMMENTS_EDIT = method(ROOT_URL + "files.comments.edit", None, None, True)

    # files
    FILES_DELETE = method(ROOT_URL + "files.delete", None, None, True)
    FILES_INFO = method(ROOT_URL + "files.info", None, None, False)
    FILES_LIST = method(ROOT_URL + "files.list", "page", "files", False)
    FILES_REVOKE_PUBLIC_URL = method(
        ROOT_URL + "files.revokePublicURL", None, None, True
    )
    FILES_SHARED_PUBLIC_URL = method(
        ROOT_URL + "files.sharedPublicURL", None, None, True
    )
    FILES_UPLOAD = method(ROOT_URL + "files.upload", None, None, False)

    # groups
    GROUPS_ARCHIVE = method(ROOT_URL + "groups.archive", None, None, True)
    GROUPS_CLOSE = method(ROOT_URL + "groups.close", None, None, False)
    GROUPS_CREATE = method(ROOT_URL + "groups.create", None, None, True)
    GROUPS_CREATE_CHILD = method(ROOT_URL + "groups.createChild", None, None, False)
    GROUPS_HISTORY = method(ROOT_URL + "groups.history", "timeline", "messages", False)
    GROUPS_INFO = method(ROOT_URL + "groups.info", None, None, False)
    GROUPS_INVITE = method(ROOT_URL + "groups.invite", None, None, True)
    GROUPS_KICK = method(ROOT_URL + "groups.kick", None, None, True)
    GROUPS_LEAVE = method(ROOT_URL + "groups.leave", None, None, True)
    GROUPS_LIST = method(ROOT_URL + "groups.list", None, None, False)
    GROUPS_MARK = method(ROOT_URL + "groups.mark", None, None, True)
    GROUPS_OPEN = method(ROOT_URL + "groups.open", None, None, True)
    GROUPS_RENAME = method(ROOT_URL + "groups.rename", None, None, True)
    GROUPS_REPLIES = method(ROOT_URL + "groups.replies", None, None, False)
    GROUPS_SET_PURPOSE = method(ROOT_URL + "groups.setPurpose", None, None, True)
    GROUPS_SET_TOPIC = method(ROOT_URL + "groups.setTopic", None, None, True)
    GROUPS_UNARCHIVE = method(ROOT_URL + "groups.unarchive", None, None, True)

    # im
    IM_CLOSE = method(ROOT_URL + "im.close", None, None, True)
    IM_HISTORY = method(ROOT_URL + "im.history", "timeline", "messages", False)
    IM_LIST = method(ROOT_URL + "im.list", None, None, False)
    IM_MARK = method(ROOT_URL + "im.mark", None, None, True)
    IM_OPEN = method(ROOT_URL + "im.open", None, None, True)
    IM_REPLIES = method(ROOT_URL + "im.replies", None, None, False)

    # mpim
    MPIM_CLOSE = method(ROOT_URL + "mpim.close", None, None, True)
    MPIM_HISTORY = method(ROOT_URL + "mpim.history", "timeline", "messages", False)
    MPIM_LIST = method(ROOT_URL + "mpim.list", None, None, False)
    MPIM_MARK = method(ROOT_URL + "mpim.mark", None, None, True)
    MPIM_OPEN = method(ROOT_URL + "mpim.open", None, None, True)
    MPIM_REPLIES = method(ROOT_URL + "mpim.replies", None, None, False)

    # oauth
    OAUTH_ACCESS = method(ROOT_URL + "oauth.access", None, None, False)
    OAUTH_TOKEN = method(ROOT_URL + "oauth.token", None, None, False)

    # pins
    PINS_ADD = method(ROOT_URL + "pins.add", None, None, True)
    PINS_LIST = method(ROOT_URL + "pins.list", None, None, False)
    PINS_REMOVE = method(ROOT_URL + "pins.remove", None, None, True)

    # reactions
    REACTIONS_ADD = method(ROOT_URL + "reactions.add", None, None, True)
    REACTIONS_GET = method(ROOT_URL + "reactions.get", None, None, False)
    REACTIONS_LIST = method(ROOT_URL + "reactions.list", "page", "items", False)
    REACTIONS_REMOVE = method(ROOT_URL + "reactions.remove", None, None, True)

    # reminders
    REMINDERS_ADD = method(ROOT_URL + "reminders.add", None, None, True)
    REMINDERS_COMPLETE = method(ROOT_URL + "reminders.complete", None, None, True)
    REMINDERS_DELETE = method(ROOT_URL + "reminders.delete", None, None, True)
    REMINDERS_INFO = method(ROOT_URL + "reminders.info", None, None, False)
    REMINDERS_LIsT = method(ROOT_URL + "reminders.list", None, None, False)

    # rtm
    RTM_CONNECT = method(ROOT_URL + "rtm.connect", None, None, False)
    RTM_START = method(ROOT_URL + "rtm.start", None, None, False)

    # search
    SEARCH_ALL = method(ROOT_URL + "search.all", "page", "messages", False)
    SEARCH_FILES = method(ROOT_URL + "search.files", "page", "files", False)
    SEARCH_MESSAGES = method(ROOT_URL + "search.messages", "page", "messages", False)

    # starts
    STARS_ADD = method(ROOT_URL + "stars.add", None, None, True)
    STARS_LIST = method(ROOT_URL + "stars.list", "page", "items", False)
    STARS_REMOVE = method(ROOT_URL + "stars.remove", None, None, True)

    # team
    TEAM_ACCESS_LOGS = method(ROOT_URL + "teams.accessLogs", None, None, False)
    TEAM_BILLABLE_INFO = method(ROOT_URL + "teams.billableInfo", None, None, False)
    TEAM_INFO = method(ROOT_URL + "teams.info", None, None, False)
    TEAM_INTEGRATION_LOGS = method(
        ROOT_URL + "teams.integrationLogs", None, None, False
    )

    # team profile
    TEAM_PROFILE_GET = method(ROOT_URL + "teams.profile.get", None, None, False)

    # usergroups
    USERGROUPS_CREATE = method(ROOT_URL + "usergroups.create", None, None, True)
    USERGROUPS_DISABLE = method(ROOT_URL + "usergroups.disable", None, None, True)
    USERGROUPS_ENABLE = method(ROOT_URL + "usergroups.enable", None, None, True)
    USERGROUPS_LIST = method(ROOT_URL + "usergroups.list", None, None, False)
    USERGROUPS_UPDATE = method(ROOT_URL + "usergroups.update", None, None, True)

    # usergroups users
    USERGROUPS_USERS_LIST = method(
        ROOT_URL + "usergroups.users.list", None, None, False
    )
    USERGROUPS_USERS_UPDATE = method(
        ROOT_URL + "usergroups.users.update", None, None, True
    )

    # users
    USERS_DELETE_PHOTO = method(ROOT_URL + "users.deletePhoto", None, None, False)
    USERS_GET_PRESENCE = method(ROOT_URL + "users.getPresence", None, None, False)
    USERS_IDENTITY = method(ROOT_URL + "users.identity", None, None, False)
    USERS_INFO = method(ROOT_URL + "users.info", None, None, False)
    USERS_LIST = method(ROOT_URL + "users.list", "cursor", "members", False)
    USERS_SET_ACTIVE = method(ROOT_URL + "users.setActive", None, None, True)
    USERS_SET_PHOTO = method(ROOT_URL + "users.setPhoto", None, None, False)
    USERS_SET_PRESENCE = method(ROOT_URL + "users.setPresence", None, None, True)

    # users profile
    USERS_PROFILE_GET = method(ROOT_URL + "users.profile.get", None, None, False)
    USERS_PROFILE_SET = method(ROOT_URL + "users.profile.set", None, None, True)
