from typing import List, Dict, Any
from pydantic import BaseModel, Field
import enum

class Response_Models_Type(BaseModel):
    Checkpoint = "Checkpoint"
    TextualInversion = "TextualInversion"
    Hypernetwork = "Hypernetwork"
    AestheticGradient = "AestheticGradient"
    LORA = "LORA"
    Controlnet = "Controlnet"
    Poses = "Poses"

class Response_Models_Mode(BaseModel):
    Archived = "Archived"
    TakenDown = "TakenDown"

class Response_Models_Creator(BaseModel):
    username: str 	# The name of the creator
    image: str | None 	# The url of the creators avatar

class Response_Models_Stats(BaseModel):
    downloadCount: int # The number of downloads the model has
    favoriteCount: int # The number of favorites the model has
    commentCount: int # The number of comments the model has
    ratingCount: int # The number of ratings the model has
    rating: float	# The average rating of the model

class Response_Models_modelVersions_Files_Metadata_fp(enum.Enum):
    fp16 = "fp16"
    fp32 = "fp32"

class Response_Models_modelVersions_Files_Metadata_Size(BaseModel):
    full = "full"
    pruned = "pruned"

class Response_Models_modelVersions_Files_Metadata_Format(BaseModel):
    SafeTensor = "SafeTensor"
    PickleTensor = "PickleTensor"
    Other = "Other"

class Response_Models_modelVersions_Files_Metadata(BaseModel):
    fp: Response_Models_modelVersions_Files_Metadata_fp | None # The specified floating point for the file
    size: Response_Models_modelVersions_Files_Metadata_Size | None # The specified model size for the file
    format: Response_Models_modelVersions_Files_Metadata_Format | None 	# The specified model format for the file


class Response_Models_modelVersions_Files_PickleScanResult(enum.Enum):
    Pending = 'Pending'
    Success = 'Success'
    Danger = 'Danger'
    Error = 'Error'
    
class Response_Models_modelVersions_Files_VirusScanResult(enum.Enum):
    Pending = 'Pending'
    Success = 'Success'
    Danger = 'Danger'
    Error = 'Error'

class Response_Models_modelVersions_Files_Hashes(BaseModel):
    AutoV2: str
    SHA256: str
    CRC32: str
    BLAKE3: str

class Response_Models_modelVersions_Files(BaseModel):
    name: str # file name
    id: int # file id
    sizeKb: float # The size of the model file
    metadata: Response_Models_modelVersions_Files_Metadata
    pickleScanResult: Response_Models_modelVersions_Files_PickleScanResult # Status of the pickle scan ('Pending', 'Success', 'Danger', 'Error')
    virusScanResult: Response_Models_modelVersions_Files_VirusScanResult # Status of the virus scan ('Pending', 'Success', 'Danger', 'Error')
    scannedAt: str | None # (ISO 8601) The date in which the file was scanned
    hashes: Response_Models_modelVersions_Files_Hashes
    downloadUrl: str # model download url: "https://civitai.com/api/download/models/8387"
    primary: bool | None # If the file is the primary file for the model version

class Response_Models_modelVersions_Images_Meta(BaseModel):
    ENSD: str # stringified number
    Size: str # resolution string 
    seed: int
    Score: str # float string
    steps: int
    prompt: str
    sampler: str
    Eta_DDIM: str = Field(alias="Eta DDIM") # float string
    cfgScale: int
    resources: List[Any]
    Model_hash: str = Field(alias="Model hash") # short hash string
    Hires_upscale: str = Field(alias="Hires upscale") # float str
    Hires_upscaler: str = Field(alias="Hires upscaler") # hires upscaler name
    negativePrompt: str
    Denoising_strength: str = Field(alias="Denoising strength") # float string

class Response_Models_modelVersions_Images(BaseModel):
    url: str 	# The url for the image
    nsfw: bool 	# Whether or not the image is NSFW (note: if the model is NSFW, treat all images on the model as NSFW)
    width: int 	# The original width of the image
    height: int 	# The original height of the image
    hash: str 	#The blurhash of the image
    meta: Response_Models_modelVersions_Images_Meta | None 	# The generation params of the image

class Response_Models_modelVersions_Stats(BaseModel):
    downloadCount: int # The number of downloads the model has
    ratingCount: int # The number of ratings the model has
    rating: float # The average rating of the model

class Response_Models_modelVersions(BaseModel):
    id: int	# The identifier for the model version
    modelId: int # The model id
    baseModel: str # The base model of the model
    name: str # The name of the model version
    description: str # The description of the model version (usually a changelog)
    createdAt: str 	# (ISO 8601) The date in which the version was created
    updatedAt: str  # (ISO 8601) The date in which the version was updated
    downloadUrl: str 	# The download url to get the model file for this specific version
    trainedWords: List[str] 	# The words used to trigger the model
    files: List[Response_Models_modelVersions_Files]
    images: List[Response_Models_modelVersions_Images]
    stats: Response_Models_modelVersions_Stats

class Response_Models_Metadata(BaseModel):
    totalItems: int 	# The total number of items available
    currentPage: int 	# The the current page you are at
    pageSize: int 	# The the size of the batch
    totalPages: int 	# The total number of pages
    nextPage: str | None	# The url to get the next batch of items
    prevPage: str | None	# The url to get the previous batch of items

class Response_Model(BaseModel):
    id: int 	# The identifier for the model
    name: str 	# The name of the model
    description: str 	# The description of the model (HTML)
    type: Response_Models_Type # The model type
    nsfw: bool # Whether the model is NSFW or not
    tags: List[str] # The tags associated with the model
    mode: Response_Models_Mode | None 	# The mode in which the model is currently on. If Archived, files field will be empty. If TakenDown, images field will be empty
    creator: Response_Models_Creator
    stats: Response_Models_Stats
    modelVersions: List[Response_Models_modelVersions]

class Response_Models(BaseModel):
    items: List[Response_Model]
    metadata: Response_Models_Metadata
