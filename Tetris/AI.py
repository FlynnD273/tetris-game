import keras
import numpy as np

from .Tile import Tile
from .Game import Actions

# from .Board import Board
from .Mino import Mino

# from keras.utils import CustomObjectScope
# from keras.metrics import Precision , Recall


class AI:
    """The AI. Geneticly trained"""

    def __init__(self, file="") -> None:
        if file:
            # with CustomObjectScope(
            #     {
            #         "binary_precision": Precision(),
            #         "binary_recall": Recall(),
            #     }
            # ):
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
        dense_layer3 = keras.layers.Dense(
            10, activation="relu", use_bias=True, name="dense3"
        )(dense_layer2)
        output_layer = keras.layers.Dense(6, activation="softmax")(dense_layer3)

        model = keras.Model(inputs=input_board, outputs=output_layer, name="AI")
        # keras.utils.plot_model(model, to_file="test.png", show_shapes=True)
        return model

    def get_action(self, board: list[Tile], mino: Mino) -> int:
        """get the AI's action to  play, returns 0..6"""
        board_one = map(lambda x: 0 if x == Tile.Clear else 1, board)
        board_shape = np.array(list(board_one)).reshape((1, 20, 10))

        # a board with only the current piece
        piece_grid = np.array(mino.currTiles).reshape((4, 4)) * -1
        start = mino.offset
        for x in range(0, 4):
            for y in range(0, 4):
                offset = (y + start[0], x + start[1])
                if 0 <= offset[0] < 20 and 0 <= offset[1] < 10:
                    board_shape[0, offset[0], offset[1]] = piece_grid[y, x]
        predict = self.model.predict(board_shape, verbose="0")
        return int(np.argmax(predict))

