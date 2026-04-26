from datetime import date, timedelta

from app.services.kpi import deal_overdue


def test_deal_overdue_true():
    assert deal_overdue(date.today() - timedelta(days=1)) is True


def test_deal_overdue_false():
    assert deal_overdue(date.today() + timedelta(days=1)) is False
