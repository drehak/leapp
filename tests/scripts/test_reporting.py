from leapp.actors import Actor
from leapp.messaging.inprocess import InProcessMessaging
from leapp.reporting import Renderers, Report, report
from leapp.tags import Tag

from helpers import repository_dir

import json
import pytest


class HuhTag(Tag):
    name = "huh"


class Huh(Actor):
    name = "huh"
    consumes = ()
    produces = (Report,)
    tags = (HuhTag,)

    def process(self):
        pass


def test_heritability():
    with pytest.raises(TypeError):
        class SubReport(Report):
            pass


rend = Renderers(html="heck yes", plaintext="hell yeah")

def test_minimal(repository_dir):
    with repository_dir.as_cwd():
        mailbox = InProcessMessaging()
        actor = Huh(messaging=mailbox)
        report(title="title", detail={}, renderers=rend.dump())

@pytest.mark.parametrize("severity", ("low", "medium", "high", "", None))
def test_severity_ok(severity, repository_dir):
    with repository_dir.as_cwd():
        mailbox = InProcessMessaging()
        actor = Huh(messaging=mailbox)
        report(title="title", detail={}, renderers=rend.dump(), severity=severity)
        data = mailbox.messages()[0]["message"]["data"]
        assert(not severity or '"severity": "{}"'.format(severity in data))
        assert False

@pytest.mark.parametrize("severity", ("extreme", 123))
def test_severity_wrong(severity, repository_dir):
    with pytest.raises(Exception):
        with repository_dir.as_cwd():
            mailbox = InProcessMessaging()
            actor = Huh(messaging=mailbox)
            report(title="title", detail={}, renderers=rend.dump(), severity=severity)

@pytest.mark.parametrize("audience", ([], ["developer"], ["sysadmin"], ["developer", "sysadmin"]))
def test_audience_ok(audience, repository_dir):
    with repository_dir.as_cwd():
        mailbox = InProcessMessaging()
        actor = Huh(messaging=mailbox)
        report(title="title", detail={}, renderers=rend.dump(), audience=audience)
        data = mailbox.messages()[0]["message"]["data"]
        assert('"severity": "{}"'.format(str(audience).replace("'", '"')) in data)

@pytest.mark.parametrize("audience", (["user"], [123]))
def test_audience_wrong(audience, repository_dir):
    with pytest.raises(Exception):
        with repository_dir.as_cwd():
            mailbox = InProcessMessaging()
            actor = Huh(messaging=mailbox)
            report(title="title", detail={}, renderers=rend.dump(), audience=audience)
