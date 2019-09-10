import vcr

vcr_instance = vcr.VCR(  # Following option is often used.
    cassette_library_dir="./tests/vcr/cassettes/",  # A Location to storing VCR Cassettes
    decode_compressed_response=True,  # Store VCR content (HTTP Requests / Responses) as a Plain text.
    serializer="json",  # Store VCR Record as a JSON Data
)
