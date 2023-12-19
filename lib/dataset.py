
import tensorflow as tf
import tensorflow_datasets as tfds


class Dataset():
    def __init__(self, seed=42, dataset_name='rock_paper_scissors'):
        self.read_config = tfds.ReadConfig(
            shuffle_seed=seed, 
            shuffle_reshuffle_each_iteration=True,
            )
        self.data_dir = '/tensorflow_datasets'
        self.ds_train_full = None
        self.ds_train = None
        self.ds_val = None
        self.ds_test = None
        self.dataset_name = dataset_name
        self.ds_train_full, self.ds_info = tfds.load(
            dataset_name, split=['train'],
            with_info=True)
        self.ds_train_full = self.ds_train_full[0]
        print(type(self.ds_train_full))


    def load(self, validation_proportion=0.15):
        # Calculate the number of validation samples (15% of training data)
        num_train_samples = self.ds_info.splits['train'].num_examples
        num_val_samples = int(num_train_samples * validation_proportion)

        # Define the new training and validation splits
        train_split = f'train[:{num_train_samples - num_val_samples}]'
        val_split = f'train[{num_train_samples - num_val_samples}:]'

        # Load the datasets
        (self.ds_train, self.ds_val, self.ds_test), self.ds_info = tfds.load(
            self.dataset_name,
            split=[train_split, val_split, 'test'],
            shuffle_files=True,
            as_supervised=True,
            with_info=True,
            read_config=self.read_config,
        )
        

    # def load_cv(self, num_folds=5):
    #     # Calculate the size of each fold
    #     num_train_samples = self.ds_info.splits['train'].num_examples
    #     fold_size = num_train_samples // num_folds

    #     # Initialize lists to store the datasets
    #     self.ds_train_folds = []
    #     self.ds_val_folds = []

    #     # Create the splits for training and validation datasets
    #     for i in range(num_folds):
    #         # Define the splits
    #         val_split = f'train[{i * fold_size}:{(i + 1) * fold_size}]'
    #         train_split = f'train[:{i * fold_size}]+train[{(i + 1) * fold_size}:]'

    #         # Load the datasets
    #         ds_train, ds_val = tfds.load(
    #             self.dataset_name,
    #             split=[train_split, val_split],
    #             shuffle_files=True,
    #             as_supervised=True,
    #             with_info=False,
    #             read_config=self.read_config,
    #         )

    #         # Store the datasets
    #         self.ds_train_folds.append(ds_train)
    #         self.ds_val_folds.append(ds_val)

    def get_ds_train(self):
        return self.ds_train
    def get_ds_val(self):
        return self.ds_val
    def get_ds_test(self):
        return self.ds_test
    