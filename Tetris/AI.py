import keras
import numpy as np

from .Tile import Tile
from .Game import Actions
# from .Board import Board
from .Mino import Mino


class AI:
    """The AI. Geneticly trained"""

    def __init__(self, file="") -> None:
        if file:
            self.model: keras.Model = keras.models.load_model(file)
        else:
            self.model: keras.Model = self.build_new_model()

    def build_new_model() -> keras.Model:
        board_size = (10, 20)

        input_board = keras.layers.Input(board_size)
        input_piece = keras.layers.Input(board_size)
        conv_layer1 = keras.layers.Conv2D(10, (3, 3), activation="relu")(input_board)
        conv_layer2 = keras.layers.Conv2D(10, (3, 3), activation="relu")(input_piece)
        merge_layer = keras.layers.Concatenate(axis=1)([conv_layer1, conv_layer2])
        dense_layer1 = keras.layers.Dense(10, activation="sigmoid", use_bias=True)(
            merge_layer
        )
        dense_layer2 = keras.layers.Dense(10, activation="relu", use_bias=True)(
            dense_layer1
        )
        output_layer = keras.layers.Dense(6, activation="softmax")(dense_layer2)

        return keras.Model(inputs=[input_board, input_piece], outputs=output_layer)

    def get_action(self, board: list[Tile], mino: Mino) -> int:
        board_one = map(lambda x: 0 if x == Tile.Clear else 1, board)
        # the board
        board_shape = np.shape(board_one, (10, 20))

        # a board with only the current piece
        piece_board = np.zeros((10, 20))
        piece_grid = np.reshape(mino.currTiles(), (4, 4))

        end = (mino.offset[0] + 4, mino.offset[1] + 4)

        piece_board[mino.offset[0] : end[0], mino.offset[1] : end[1]] = piece_grid

        return self.model.predict(
            [
                board_shape,
                piece_board,
            ]
        )
