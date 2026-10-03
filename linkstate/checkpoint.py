from copy import deepcopy
from dataclasses import asdict
from .transport import Transport


def export_checkpoint(sim):
    return deepcopy(
        {
            "schema": 1,
            "tick": sim.tick,
            "period": sim.reflood_period,
            "edges": [[*sorted(key), cost] for key, cost in sim.link_costs.items()],
            "routers": {
                rid: {
                    "links": dict(r.local_links),
                    "lsdb": r.lsdb_snapshot(),
                    "lifetime": r.lifetime,
                }
                for rid, r in sim.routers.items()
            },
            "history": [asdict(record) for record in sim.history],
        }
    )


def restore_checkpoint(cls, data):
    edges = {(a, b): cost for a, b, cost in data["edges"]}
    lifetime = next(iter(data["routers"].values()))["lifetime"]
    sim = cls(edges, Transport(), data["period"], lifetime)
    for rid, row in data["routers"].items():
        sim.routers[rid].update_local_links(row["links"])
    return sim
