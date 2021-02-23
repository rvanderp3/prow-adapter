from gather_resource_to_files import GatherResourceToFiles

class GatherPVs(GatherResourceToFiles):
    def __init__(self):
        GatherResourceToFiles.__init__(self,'gather-extra/artifacts/persistentvolumes.json',
                                'cluster-scoped-resources/core/persistentvolumes')