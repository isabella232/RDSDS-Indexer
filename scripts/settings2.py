OMICSDI = {
  'base_url': "https://www.omicsdi.org/ws/dataset/search?",
  'metabolights': {
    'query': "repository:\"Metabolights\"",
    'dataset_url': "http://www.ebi.ac.uk/metabolights/{}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/metabolights_dataset/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/metabolights_dataset/{}.json",
  },
  'pride': {
    'query': "repository:\"Pride\"",
    'dataset_url': "http://www.ebi.ac.uk/pride/archive/projects/{}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/pride/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/pride/{}.json"
  },
  'arrayexpress': {
    'query': "repository:\"ArrayExpress\"",
    'dataset_url': "https://www.ebi.ac.uk/arrayexpress/experiments/{}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/arrayexpress-repository/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/arrayexpress-repository/{}.json"
  },
  'eva': {
    'query': "repository:\"EVA\"",
    'dataset_url': "https://www.ebi.ac.uk/eva/?eva-study={}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/eva/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/eva/{}.json"
  },
}



















PATHS = {
  'metabolights': {
    'identifiers.org': "http://identifiers.org/metabolights:{}",
    'file': ['/ebi/ftp/pub/databases/metabolights/studies/public/{}'],
    'https': ['https://www.ebi.ac.uk/metabolights/{}/files/'],
    'ftp': [
      'ftp://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/{}'
      'ftp://hh-gridftp-1.ebi.ac.uk:2811/gridftp/pub/databases/metabolights/studies/public/{}'
      'ftp://oy-gridftp-1.ebi.ac.uk:2811/pub/databases/metabolights/studies/public/{}'
    ],
    'gsiftp': [
      'gsiftp://hh-gridftp-1.ebi.ac.uk/gridftp/pub/databases/metabolights/studies/public/{}'
      'gsiftp://oy-gridftp-1.ebi.ac.uk/pub/databases/metabolights/studies/public/{}'
    ],
    'globus': [
      'globus://ebi#public/gridftp/pub/databases/metabolights/studies/public/{}'
      'globus://9e437f9e-7e22-11e5-9931-22000b96db58/gridftp/pub/databases/metabolights/studies/public/{}'
      'globus://ebi#pub/pub/databases/metabolights/studies/public/{}'
      'globus://ddb59cc9-6d04-11e5-ba46-22000b92c6ec/pub/databases/metabolights/studies/public/{}'
      'globus://ebi#09443db8-59e6-11e9-a621-0a54e005f950/pub/databases/metabolights/studies/public/{}'
    ]
  },
  'pride': {
    'identifiers.org': "http://identifiers.org/pride:{}",
    'file': ['/nfs/public/release/pride/prod/pride/data/archive/{}'],
    'https': ['https://www.ebi.ac.uk/pride/data/archive/{}'],
    'ftp': [
      'ftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    ],
    'gsiftp': [
      'gsiftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    ],
    'globus': [
      'globus://ddb59cab-6d04-11e5-ba46-22000b92c6ec/pride/data/archive/{}',
      'globus://ebi#pride/pride/data/archive/{}'
    ],
    'aspera': [
      'prd_ascp@fasp.ebi.ac.uk:pride/data/archive/{}'
    ]
  },
  'arrayexpress': {
    'identifiers.org': "http://identifiers.org/arrayexpress:{}",
    'file': [
      '/ebi/ftp/pub/databases/arrayexpress/data/experiment/{}',
      '/ebi/ftp/pub/databases/microarray/{}'
      ],
    'https': [
      "https://www.ebi.ac.uk/arrayexpress/files/{}"
    ],
  },
  'eva': {
    'identifiers.org': "http://identifiers.org/eva:{}",
    'file': [
      '/ebi/ftp/pub/databases/arrayexpress/data/experiment/{}'
    ],
    'ftp': [
      "ftp://ftp.ebi.ac.uk/pub/databases/eva/{}"
    ]
  }
}

ACCESS_METHODS = {
  'metabolights': {
    'access_methods': [
      {
        'type': 'file',
        'access_url': '/ebi/ftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': None,
        'region': 'ebi-cli.ssh.ebi.ac.uk'
      },
      {
        'type': 'file',
        'access_url': '/ebi/ftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': None,
        'region': 'ebi-sra-1.ssh.ebi.ac.uk'
      },
      {
        'type': 'file',
        'access_url': '/nfs/ftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': None,
        'region': 'ebi-sra-2.ssh.ebi.ac.uk'
      },
      {
        'type': 'https',
        'access_url': 'https://www.ebi.ac.uk/metabolights/{bundle_name}/files/{object_path}',
        'access_id': None,
        'region': 'www.ebi.ac.uk'
      },
      {
        'type': 'ftp', 'access_url':
        'ftp://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/{bundle_path}',
        'access_id': '',
        'region': 'ftp.ebi.ac.uk'
      },
      {
        'type': 'ftp',
        'access_url': 'ftp://hh-gridftp-1.ebi.ac.uk:2811/gridftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'hh-gridftp-1.ebi.ac.uk'
      },
      {
        'type': 'ftp',
        'access_url': 'ftp://oy-gridftp-1.ebi.ac.uk:2811/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'oy-gridftp-1.ebi.ac.uk'
      },
      {
        'type': 'gsiftp',
        'access_url': 'gsiftp://hh-gridftp-1.ebi.ac.uk/gridftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'hh-gridftp-1.ebi.ac.uk'
      },
      {
        'type': 'gsiftp',
        'access_url': 'gsiftp://oy-gridftp-1.ebi.ac.uk/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'oy-gridftp-1.ebi.ac.uk'
      },
      {
        'type': 'globus',
        'access_url': '9e437f9e-7e22-11e5-9931-22000b96db58:/gridftp/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'public-globus.ebi.ac.uk'
      },
      {
        'type': 'globus',
        'access_url': 'globus://ddb59cc9-6d04-11e5-ba46-22000b92c6ec/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'pub-globus.ebi.ac.uk'
      },
      {
        'type': 'globus',
        'access_url': '09443db8-59e6-11e9-a621-0a54e005f950:/pub/databases/metabolights/studies/public/{bundle_object_path}',
        'access_id': '',
        'region': 'rdsds-globus.ebi.ac.uk'
      },
    ],
  },
  'pride': {
    'identifiers.org': "http://identifiers.org/pride:{}",
    'file': ['/nfs/public/release/pride/prod/pride/data/archive/{}'],
    'https': ['https://www.ebi.ac.uk/pride/data/archive/{}'],
    'ftp': [
      'ftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    ],
    'gsiftp': [
      'gsiftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    ],
    'globus': [
      'globus://ddb59cab-6d04-11e5-ba46-22000b92c6ec/pride/data/archive/{}',
      'globus://ebi#pride/pride/data/archive/{}'
    ],
    'aspera': [
      'prd_ascp@fasp.ebi.ac.uk:pride/data/archive/{}'
    ]
  },
  'arrayexpress': {
    'identifiers.org': "http://identifiers.org/arrayexpress:{}",
    'file': ['/ebi/ftp/pub/databases/arrayexpress/data/experiment/{}'],
    # 'https': ['https://www.ebi.ac.uk/pride/data/archive/{}'],
    # 'ftp': [
    #   'ftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    # ],
    # 'gsiftp': [
    #   'gsiftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    # ],
    # 'globus': [
    #   'globus://ddb59cab-6d04-11e5-ba46-22000b92c6ec/pride/data/archive/{}',
    #   'globus://ebi#pride/pride/data/archive/{}'
    # ],
    # 'aspera': [
    #   'prd_ascp@fasp.ebi.ac.uk:pride/data/archive/{}'
    # ]
  },
  '1000g': {
    'identifiers.org': "http://identifiers.org/1000g:{}",
    'file': ['/nfs/1000g-archive/vol1/ftp/{}'],
    # 'https': ['https://www.ebi.ac.uk/pride/data/archive/{}'],
    # 'ftp': [
    #   'ftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    # ],
    # 'gsiftp': [
    #   'gsiftp://pg-gridftp-2.ebi.ac.uk/pride/data/archive/{}'
    # ],
    # 'globus': [
    #   'globus://ddb59cab-6d04-11e5-ba46-22000b92c6ec/pride/data/archive/{}',
    #   'globus://ebi#pride/pride/data/archive/{}'
    # ],
    'aspera': [
      'fasp-g1k@fasp.1000genomes.ebi.ac.uk:vol1/ftp/{}'
    ]
  }
}