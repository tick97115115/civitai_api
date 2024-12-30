import enum
from pydantic import BaseModel

class NsfwLevel(enum.Enum):
    None = 'None'
    Soft = 'Soft'
    Mature = 'Mature'
    X = 'X'

class Sort(enum.Enum):
    Most_Reactions = "Most Reactions"
    Most_Comments = "Most Comments"
    Newest = "Newest"

class Period(enum.Enum):
    AllTime = "AllTime"
    Day = "Day"
    Week = "Week"
    Month = "Month"
    Year = "Year"

class Response_Images_Stats(BaseModel):
    cryCount: int # The number of cry reactions
    laughCount: int # The number of laugh reactions
    likeCount: int # The number of like reactions
    heartCount: int # The number of heart reactions
    commentCount: int # The number of comment reactions

class Response_Images_Meta(BaseModel):
    Size: str
    seed: int
    Model: str
    steps: int
    prompt: str
    sampler: str
    cfgScale: int
    Clip_skip: str
    Hires_upscale: str
    Hires_upscaler: str
    negativePrompt: str
    Denoising_strength: str
    #   "meta": {
    #     "Size": "512x768",
    #     "seed": 234871805,
    #     "Model": "Meina",
    #     "steps": 35,
    #     "prompt": "<lora:setsunaTokage_v10:0.6>, green hair, long hair, standing, (ribbed dress), zettai ryouiki, choker, (black eyes), looking at viewer, adjusting hair, hand in own hair, street, grin, sharp teeth, high ponytail, [Style of boku no hero academia]",
    #     "sampler": "DPM++ SDE Karras",
    #     "cfgScale": 7,
    #     "Clip skip": "2",
    #     "Hires upscale": "2",
    #     "Hires upscaler": "4x-AnimeSharp",
    #     "negativePrompt": "(worst quality, low quality, extra digits:1.3), easynegative,",
    #     "Denoising strength": "0.4"
    #   },

class Response_Images_Metadata(BaseModel):
    nextCursor: int   # The id of the first image in the next batch
    currentPage: int  	# The the current page you are at (if paging)
    pageSize: int     # The the size of the batch (if paging)
    nextPage: str      #The url to get the next batch of items

class Response_Images(BaseModel):
    id: int	#The id of the image
    url: str # The url of the image at it's source resolution
    hash: str # The blurhash of the image
    width: int # The width of the image
    height: int	# The height of the image
    nsfw: bool # If the image has any mature content labels
    nsfwLevel: NsfwLevel # The NSFW level of the image
    createdAt: str # (ISO 8601 format) The date the image was posted
    postId: int # The ID of the post the image belongs to
    stats: Response_Images_Stats
    meta: dict # this field is a non-structured object that contains additional information about the image, the meta structure will be different for each webui
    username: str # The username of the creator
    metadata: Response_Images_Metadata