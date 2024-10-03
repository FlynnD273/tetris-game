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

    def build_new_model(self) -> keras.Model:
        """Build the AI with random weights"""
        board_size = (20, 10, 1)

        input_board = keras.layers.Input(
            shape=board_size, dtype="float32", name="board"
        )
        # input_piece = keras.layers.Input(board_size, dtype="float32", name="piece")
        conv_layer1 = keras.layers.Conv2D(10, (3, 3), activation="relu", name="conv1")(
            input_board
        )
        flatten_layer = keras.layers.Flatten(name="flatten")(conv_layer1)
        # conv_layer2 = keras.layers.Conv2D(10, (3, 3), activation="relu", name="conv2")(
        #     input_piece
        # )
        # merge_layer = keras.layers.Concatenate(axis=1, name="merge")(
        #     [conv_layer1, conv_layer2]
        # )
        dense_layer1 = keras.layers.Dense(
            10, activation="sigmoid", use_bias=True, name="dense1"
        )(flatten_layer)
        dense_layer2 = keras.layers.Dense(
            10, activation="relu", use_bias=True, name="dense2"
        )(dense_layer1)
        output_layer = keras.layers.Dense(6, activation="softmax")(dense_layer2)

        model = keras.Model(inputs=input_board, outputs=output_layer, name="AI")
        keras.utils.plot_model(model, to_file="test.png", show_shapes=True)
        return model

    def get_action(self, board: list[Tile], mino: Mino) -> int:
        """get the AI's action to  play, returns 0..6""" 
        board_one = list(map(lambda x: 0 if x == Tile.Clear else 1, board))
        # the board
        board_shape = np.array(board_one).reshape((1, 20, 10))

        # a board with only the current piece
        # piece_board = np.zeros((10, 20, 1))
        piece_grid = np.array(mino.currTiles).reshape((4, 4)) * -1
        # print(list(mino.currTiles))
        # print(list(piece_grid))
        start = mino.offset
        # breakpoint()
        for x in range(0, 4):
            for y in range(0, 4):
                offset = (y + start[0], x + start[1])
                if 0 <= offset[0] < 20 and 0 <= offset[1] < 10:
                    board_shape[0, offset[0], offset[1]] = piece_grid[y, x]
        # print(board_shape)
        # print(start)
        predict = self.model.predict(board_shape, verbose=0)
        # print(predict)
        return np.argmax(predict)
