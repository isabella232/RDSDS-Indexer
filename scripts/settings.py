OMICSDI = {
  'base_url': "https://www.omicsdi.org/ws/dataset/search?",
  'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/{}/{}.json",
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
  'expression-atlas': {
    'query': "repository:\"ExpressionAtlas\"",
    'dataset_url': "http://www.ebi.ac.uk/gxa/experiments/{}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/atlas-experiments/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/atlas-experiments/{}.json"
  },
  'biomodels': {
    'query': "repository:\"BioModels\"",
    'dataset_url': "https://www.ebi.ac.uk/biomodels/{}",
    'omicsdi_url': "https://www.omicsdi.org/dataset/biomodels/{}",
    'omicsdi_api_url': "https://www.omicsdi.org/ws/dataset/biomodels/{}.json"
  },
  'ena': {
    'query': "repository:\"ENA\"",
  },
}


OMICSDI_HEADERS = ['dataset', 'id', 'pub_date' , 'dataset_url',
                   'omicsdi_url', 'omicsdi_api_url','local_path']

HASH_HEADERS = ["type","id","name","dataset","bundle","size","timestamp",
                "crc32c","md5","sha256","sha512","trunc512","blake2b",
                "contents"]





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
      '/ebi/ftp/pub/databases/microarray/data/experiment/{}'
      ],
    'https': [
      "https://www.ebi.ac.uk/arrayexpress/files/{}"
    ],
  },
  'eva': {
    'file': ['/ebi/ftp/pub/databases/eva/{}'],
    'ftp': ["ftp://ftp.ebi.ac.uk/pub/databases/eva/{}"],
    'globus': ["globus://6f70c1b4-b824-11e9-98d7-0a63aa6b37da:/gridftp/pub/databases/eva/{}"]
  },
  'expression-atlas': {
    'file': [
      '/ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      '/ebi/ftp/pub/databases/microarray/data/atlas/experiments/{}'
    ],
    'ftp': ["ftp://ftp.ebi.ac.uk/pub/databases/arrayexpress/data/atlas/experiments/{}"]
  },
  'omics_ena_project': {
    'file': ['/nfs/era-pub/vol1/{}'],
    'ftp': ['ftp.sra.ebi.ac.uk/vol1/{}'],
    'https': ['ftp.sra.ebi.ac.uk/vol1/{}']
  }
}




ACCESS_URLS = {
  'eva': [
    { 'type': 'file',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/eva/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/eva/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'file',
      'region': 'sra-login.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/eva/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/eva/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'sftp',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/eva/{}',
      'access_url': 'sftp://ebi-cli.ebi.ac.uk/ebi/ftp/pub/databases/eva/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'ftp',
      'region': 'ftp.ebi.ac.uk',
      'path': '/ftp/pub/databases/eva/{}',
      'access_url': 'ftp://ftp.ebi.ac.uk/pub/databases/eva/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'globus',
      'region': 'globus.ebi.ac.uk',
      'path': '/gridftp/pub/databases/eva/{}',
      'access_url': 'globus://fd9c190c-b824-11e9-98d7-0a63aa6b37da:/gridftp/pub/databases/eva/{}',
      'access_id': '',
      'headers': ''
    },
  ],
  'metabolights': [
    { 'type': 'file',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'file',
      'region': 'sra-login.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'sftp',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_url': 'sftp://ebi-cli.ebi.ac.uk/ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'http',
      'region': 'ftp.ebi.ac.uk',
      'path': '/pub/databases/metabolights/studies/public/{}',
      'access_url': 'https://www.ebi.ac.uk/metabolights/{}/files/',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'ftp',
      'region': 'ftp.ebi.ac.uk',
      'path': '/pub/databases/metabolights/studies/public/{}',
      'access_url': 'ftp://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'globus',
      'region': 'globus.ebi.ac.uk',
      'path': '/gridftp/pub/databases/eva/{}',
      'access_url': 'globus://fd9c190c-b824-11e9-98d7-0a63aa6b37da:/gridftp/pub/databases/metabolights/studies/public/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'aspera',
      'region': 'fasp.ebi.ac.uk',
      'path': '/studies/public/{}',
      'access_url': 'fasp://fasp_ml@fasp.ebi.ac.uk/studies/public/{}',
      'access_id': 'asperaweb_id_dsa.openssh',
      'headers': ''
    },
  ],
  'expression-atlas': [
    { 'type': 'file',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'file',
      'region': 'sra-login.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/metabolights/studies/public/{}',
      'access_url': 'file:///ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'sftp',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_url': 'sftp://ebi-cli.ebi.ac.uk/ebi/ftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'ftp',
      'region': 'ftp.ebi.ac.uk',
      'path': '/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_url': 'ftp://ftp.ebi.ac.uk/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'globus',
      'region': 'globus.ebi.ac.uk',
      'path': '/gridftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_url': 'globus://fd9c190c-b824-11e9-98d7-0a63aa6b37da:/gridftp/pub/databases/arrayexpress/data/atlas/experiments/{}',
      'access_id': '',
      'headers': ''
    },
  ],
  'ena': [
    { 'type': 'file',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp/era-pub/{}',
      'access_url': 'file:///ebi/ftp/era-pub/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'file',
      'region': 'sra-login.ebi.ac.uk',
      'path': '/ebi/ftp/era-pub/{}',
      'access_url': 'file:///ebi/ftp/era-pub/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'sftp',
      'region': 'ebi-cli.ebi.ac.uk',
      'path': '/ebi/ftp//era-pub/{}',
      'access_url': 'sftp://ebi-cli.ebi.ac.uk/ebi/ftp/era-pub/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'ftp',
      'region': 'ftp.era.ebi.ac.uk',
      'path': '/vol1/era-pub/{}',
      'access_url': 'ftp://ftp.era.ebi.ac.uk/vol1/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'ftp',
      'region': 'ftp.ebi.ac.uk',
      'path': '/era-pub/{}',
      'access_url': 'ftp://ftp.ebi.ac.uk/era-pub/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'gsiftp',
      'region': 'gsiftp.ebi.ac.uk',
      'path': '/era-pub/{}',
      'access_url': 'gsiftp://hx-gridftp-8.ebi.ac.uk/era-pub/{}',
      'access_id': '',
      'headers': ''
    },
    { 'type': 'globus',
      'region': 'globus.ebi.ac.uk',
      'path': '/gridftp/ena/{}',
      'access_url': 'globus://fd9c190c-b824-11e9-98d7-0a63aa6b37da:/gridftp/ena/{}',
      'access_id': '',
      'headers': ''
    },
  ],
}