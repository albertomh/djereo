from typing import TypedDict


class MailPitEmailAddress(TypedDict):
    Name: str
    Address: str


class MailPitMessage(TypedDict):
    ID: str
    MessageID: str
    Read: bool
    From: MailPitEmailAddress
    To: list[MailPitEmailAddress]
    Cc: None | list[MailPitEmailAddress]
    Bcc: None | list[MailPitEmailAddress]
    ReplyTo: list[MailPitEmailAddress]
    Subject: str
    Created: str
    Username: str
    Tags: list[str]
    Size: int
    Attachments: int
    Snippet: str
