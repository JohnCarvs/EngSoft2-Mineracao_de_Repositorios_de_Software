import re
from collections import defaultdict
from typing import Dict

from analyzer.models import MinedRepo, MetricResult


def analyze(repo: MinedRepo) -> MetricResult:
    result = defaultdict(float, 0.)

    return result

