#kif

Seeing as this bot is mostly for fun we are going to have some restrictions.

1. kif should try to hold as little in running memory as possible
 - Whenever possible save information in local files
2. Along with this kif should not lose functionality on a restart
 - Take advantage of the local file system to avoid redoing calculations/queries
 - Try to use get_or_create when applicable
 - Treat each event as progressing kif along a state machine
    - So that events can happen even if kif restarts constantly
3. Instead of hard coding or class level variables, use config files when possible
 - Not only does this help with testing, but it makes it easier to port kif to other slacks
4. Use handlers for processing events
 - These are going to eventually have an interface and will be possible to enable/disable from slack
5. For completely arbitrary reasons kif is not capitalized.
 - sigh