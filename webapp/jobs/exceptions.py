class JobsError(Exception):
    """Base exception class for all jobs app related errors.
    """

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class OpeningExistError(JobsError):
    """Error thrown when job url for an opening being inserted matching those of
    an existing opening.
    """

    def __init__(self, job_url):
        errmsg = f"Opening with job url already exist. Url: {job_url}"
        JobsError.__init__(self, errmsg)
