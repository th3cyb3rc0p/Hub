"""
License:
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from typing import Tuple

from hub.schema import Tensor


class Video(Tensor):
    """`HubSchema` for videos, encoding frames individually on disk.

    The connector accepts as input a 4 dimensional `uint8` array
    representing a video.

    Returns
    ----------
    Tensor: shape [num_frames, height, width, channels],
         where channels must be 1 or 3
    """

    def __init__(
        self,
        shape: Tuple[int, ...] = (None, None, None, 3),
        dtype: str = "uint8",
        # TODO Add back encoding_format (probably named compress) when support for png and jpg support will be added
        max_shape: Tuple[int, ...] = None,
        # ffmpeg_extra_args=(),
        chunks=None,
        compressor="lz4",
    ):
        """Initializes the connector.

        Parameters
        ----------

        shape: tuple of ints
            The shape of the video (num_frames, height, width,
            channels), where channels is 1 or 3.
        dtype: `uint16` or `uint8` (default)
        max_shape : Tuple[int]
            Maximum shape of tensor if tensor is dynamic
        chunks : Tuple[int] | True
            Describes how to split tensor dimensions into chunks (files) to store them efficiently.
            It is anticipated that each file should be ~16MB.
            Sample Count is also in the list of tensor's dimensions (first dimension)
            If default value is chosen, automatically detects how to split into chunks

        Raises
        ----------
        ValueError: If the shape, dtype or encoding formats are invalid
        """
        self._check_shape(shape)
        super(Video, self).__init__(
            dtype=dtype,
            shape=shape,
            max_shape=max_shape,
            chunks=chunks,
            compressor=compressor,
        )

    def __str__(self):
        out = super().__str__()
        out = "Video" + out[6:]
        return out

    def __repr__(self):
        return self.__str__()

    def _check_shape(self, shape):
        """Check if provided shape matches Video characteristics."""
        if len(shape) != 4 or shape[-1] not in [1, 3]:
            raise ValueError(
                "Wrong Video shape provided, should be of the format (num_frames, height, width, channels), where num_frames, height, width can be integer or None and channels is 1 or 3"
            )
