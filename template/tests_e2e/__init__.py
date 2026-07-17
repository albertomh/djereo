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
    Cc: list[MailPitEmailAddress] | None
    Bcc: list[MailPitEmailAddress] | None
    ReplyTo: list[MailPitEmailAddress]
    Subject: str
    Created: str
    Username: str
    Tags: list[str]
    Size: int
    Attachments: int
    Snippet: str
