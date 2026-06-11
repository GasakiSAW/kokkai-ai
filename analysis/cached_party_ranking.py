from analysis.cache import load_json, save_json
from analysis.party_ranking import create_party_ranking


def get_cached_party_ranking():

    cache = load_json("data/party_ranking_cache.json")

    if "ranking" in cache:
        return cache["ranking"]

    ranking = create_party_ranking()

    cache["ranking"] = ranking
    save_json("data/party_ranking_cache.json", cache)

    return ranking
