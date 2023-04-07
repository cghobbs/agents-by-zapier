from urllib.parse import urlparse


def validate_request(request,
                     required_keys,
                     optional_keys=None,
                     url_keys=None):
  """
    Validate request data based on required keys, optional keys, and URL keys.

    :param request: The request object.
    :param required_keys: A list of keys that must be present in the data.
    :param optional_keys: A dictionary of optional keys with their default values.
    :param url_keys: A list of keys that must contain valid URLs.
    :return: A tuple containing a boolean indicating success, the validated data, and an error message.
    """
  # Get the POST data
  data = request.get_json()

  if optional_keys is None:
    optional_keys = {}
  if url_keys is None:
    url_keys = []

  # Initialize the validated data with default values for optional keys
  validated_data = optional_keys.copy()

  # Check for the presence of required keys
  for key in required_keys:
    if key not in data or not isinstance(data[key],
                                         str) or not data[key].strip():
      return False, None, {
        'error': f'The "{key}" value must be a non-empty string.'
      }

    # Validate URLs if the key is in the list of URL keys
    if key in url_keys:
      parsed_url = urlparse(data[key])
      if not parsed_url.scheme or not parsed_url.netloc:
        return False, None, {
          'error': f'The "{key}" value must be a valid website URL.'
        }

    # Add the value to the validated data
    validated_data[key] = data[key]

  return True, validated_data, None
