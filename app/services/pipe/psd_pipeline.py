# psd_pipeline

def get_pipeline_subsystem(subsystem_id):
    pipeline = [
        # Bước 1: Tìm tài liệu Subsystem theo _id
        {
            '$match': {'_id': subsystem_id}
        },
        # Bước 2: Lookup cho mỗi trường trong filterConditions
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.station',
                'foreignField': '_id',
                'as': 'stationData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDefinition',
                'localField': 'filterConditions.definition',
                'foreignField': '_id',
                'as': 'deviceTypeData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.kV',
                'foreignField': '_id',
                'as': 'kVData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.owner',
                'foreignField': '_id',
                'as': 'ownerData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.zone',
                'foreignField': '_id',
                'as': 'zoneData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.area',
                'foreignField': '_id',
                'as': 'areaData'
            }
        },
        {
            '$lookup': {
                'from': 'PowerSystemDataEditor',
                'localField': 'filterConditions.powerSytem',
                'foreignField': '_id',
                'as': 'elementData'
            }
        },
        # Bước 3: Dựng lại filterConditions với các đối tượng thay vì ID
        {
            '$project': {
                '_id': 1,
                'projectId': 1,
                'versionId': 1,
                'type': 1,
                'name': 1,
                'listPowerSystemId': 1,
                'active': 1,
                'filterConditions': {
                    'station': {
                        '$map': {
                            'input': '$stationData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    },
                    'definition': {
                        '$map': {
                            'input': '$deviceTypeData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.name'}
                        }
                    },
                    'kV': {
                        '$map': {
                            'input': '$kVData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    },
                    'owner': {
                        '$map': {
                            'input': '$ownerData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    },
                    'zone': {
                        '$map': {
                            'input': '$zoneData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    },
                    'area': {
                        '$map': {
                            'input': '$areaData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    },
                    'powerSytem': {
                        '$map': {
                            'input': '$elementData',
                            'as': 'item',
                            'in': {'_id': '$$item._id', 'name': '$$item.generalInfo.name'}
                        }
                    }
                }
            }
        }
    ]
    return pipeline


# Optimized get_pipeline_monitor function

def get_pipeline_monitor():
    pipeline = [
        {
            "$lookup": {
                "from": "PowerSystemDefinition",
                "localField": "engineInfo.powerSystemDefinitionId",
                "foreignField": "_id",
                "as": "powerSystemDefinition"
            }
        },
        {"$unwind": "$powerSystemDefinition"},
        {
            "$addFields": {
                "type": "$powerSystemDefinition.name"
            }
        },
        {
            "$project": {
                "_id": 1,
                "name": "$generalInfo.name",
                "type": 1,
                "values": "$engineInfo.values"
            }
        },
        {
            "$addFields": {
                # Create IDs based on the 'type' field
                "from_bus_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsBranch", "EmsBreaker"]]},
                        {"$arrayElemAt": ["$values", {
                            "$cond": [{"$eq": ["$type", "EmsBranch"]}, 3, 2]}]},
                        None
                    ]
                },
                "to_bus_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsBranch", "EmsBreaker"]]},
                        {"$arrayElemAt": ["$values", {
                            "$cond": [{"$eq": ["$type", "EmsBranch"]}, 4, 3]}]},
                        None
                    ]
                },
                "from_node_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsBranch", "EmsBreaker"]]},
                        {"$arrayElemAt": ["$values", {
                            "$cond": [{"$eq": ["$type", "EmsBranch"]}, 5, 4]}]},
                        None
                    ]
                },
                "to_node_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsBranch", "EmsBreaker"]]},
                        {"$arrayElemAt": ["$values", {
                            "$cond": [{"$eq": ["$type", "EmsBranch"]}, 6, 5]}]},
                        None
                    ]
                },
                "sbus_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsLoad", "EmsGener", "EmsShunt"]]},
                        {"$arrayElemAt": [
                            "$values",
                            {
                                "$switch": {
                                    "branches": [
                                        {"case": {
                                            "$eq": ["$type", "EmsLoad"]}, "then": 2},
                                        {"case": {
                                            "$eq": ["$type", "EmsGener"]}, "then": 3},
                                        {"case": {
                                            "$eq": ["$type", "EmsShunt"]}, "then": 1}
                                    ],
                                    "default": None
                                }
                            }
                        ]},
                        None
                    ]
                },
                "node_id": {
                    "$cond": [
                        {"$in": ["$type", ["EmsLoad", "EmsGener", "EmsShunt"]]},
                        {"$arrayElemAt": [
                            "$values",
                            {
                                "$switch": {
                                    "branches": [
                                        {"case": {
                                            "$eq": ["$type", "EmsLoad"]}, "then": 3},
                                        {"case": {
                                            "$eq": ["$type", "EmsGener"]}, "then": 4},
                                        {"case": {
                                            "$eq": ["$type", "EmsShunt"]}, "then": 2}
                                    ],
                                    "default": None
                                }
                            }
                        ]},
                        None
                    ]
                }
            }
        },
        # Combine all IDs into a single array for lookup
        {
            "$addFields": {
                "lookup_ids": {
                    "$setUnion": [
                        [
                            "$from_bus_id",
                            "$to_bus_id",
                            "$from_node_id",
                            "$to_node_id",
                            "$sbus_id",
                            "$node_id"
                        ]
                    ]
                }
            }
        },
        # Perform a single lookup for all IDs
        {
            "$lookup": {
                "from": "PowerSystemEms",
                "let": {"ids": "$lookup_ids"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$in": ["$_id", {"$map": {"input": "$$ids", "as": "id", "in": {"$toObjectId": "$$id"}}}]}
                        }
                    },
                    {
                        "$project": {
                            "_id": 1,
                            "generalInfo.name": 1
                        }
                    }
                ],
                "as": "lookup_results"
            }
        },
        # Map lookup results back to fields
        {
            "$addFields": {
                "from_bus": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$from_bus_id"}]}
                    }
                },
                "to_bus": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$to_bus_id"}]}
                    }
                },
                "from_node": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$from_node_id"}]}
                    }
                },
                "to_node": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$to_node_id"}]}
                    }
                },
                "sbus": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$sbus_id"}]}
                    }
                },
                "node": {
                    "$filter": {
                        "input": "$lookup_results",
                        "as": "item",
                        "cond": {"$eq": ["$$item._id", {"$toObjectId": "$node_id"}]}
                    }
                }
            }
        },
        # Build the 'data' field based on 'type'
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "name": 1,
                "type": 1,
                "data": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {"$in": ["$type", ["EmsBreaker", "EmsBranch"]]},
                                "then": [
                                    {
                                        "name": {
                                            "$concat": [
                                                {"$arrayElemAt": [
                                                    "$from_bus.generalInfo.name", 0]},
                                                ".",
                                                {"$arrayElemAt": [
                                                    "$from_node.generalInfo.name", 0]}
                                            ]
                                        },
                                        "_id": {"$toString": {"$arrayElemAt": ["$from_node._id", 0]}}
                                    },
                                    {
                                        "name": {
                                            "$concat": [
                                                {"$arrayElemAt": [
                                                    "$to_bus.generalInfo.name", 0]},
                                                ".",
                                                {"$arrayElemAt": [
                                                    "$to_node.generalInfo.name", 0]}
                                            ]
                                        },
                                        "_id": {"$toString": {"$arrayElemAt": ["$to_node._id", 0]}}
                                    }
                                ]
                            },
                            {
                                "case": {"$in": ["$type", ["EmsLoad", "EmsGener", "EmsShunt"]]},
                                "then": [
                                    {
                                        "name": {
                                            "$concat": [
                                                {"$arrayElemAt": [
                                                    "$sbus.generalInfo.name", 0]},
                                                ".",
                                                {"$arrayElemAt": [
                                                    "$node.generalInfo.name", 0]}
                                            ]
                                        },
                                        "_id": {"$toString": {"$arrayElemAt": ["$node._id", 0]}}
                                    }
                                ]
                            }
                        ],
                        "default": []
                    }
                }
            }
        }
    ]
    return pipeline
