
import numpy as np
# import theano
import theano.tensor as T
import skimage.io
# from skimage import io, filters

# TODO: I need to type this one up


def usage():
    "See print"
    print "This is a description on how to use the program...LOlz"


def load(paths):
    """
    Load all images into memory for faster processing.
    eg. paths =  = Paths.X_train)
    """
    images = np.empty(len(paths), dtype='object')
    for k, path in enumerate(paths):
        # TODO as_grey should be changed, it's not grey scale
        img = skimage.io.imread(path, as_grey=True)
        images[k] = img

    return images

# TODO: something doesn't work here.  The name and value is not gotten.
# I also think it's a bit crazy to make the dict into a generator item for
# just one iteration.
# def save(path, dict_of_files):
#     """
#     Handles the saving of data.path: path where the data should be saved
#     dict_of_files: dictionary of variable name and data.
#     """
#     [(name, values) in dict_of_files.iteritems()]
#     print "Saving %s in %s" % (name, path)
#     str_save = join(path,name)+".npy"
#     np.save(str_save ,getattr(Paths, name))
#     print "Gzipping %s" % name
#     system("gzip " + str_save )


def isString(s):
    return isinstance(s, basestring)


def cutoff(x):
    return T.clip(x, 0, 4)


def scaled_sigmoid(x, margin=0.5):
    return T.nnet.sigmoid(x) * (4 + 2 * margin) - margin



import numpy as np


def confusion_matrix(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Returns the confusion matrix between rater's ratings
    """
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(rater_a + rater_b)
    if max_rating is None:
        max_rating = max(rater_a + rater_b)
    num_ratings = int(max_rating - min_rating + 1)
    conf_mat = [[0 for i in range(num_ratings)]
                for j in range(num_ratings)]
    for a, b in zip(rater_a, rater_b):
        conf_mat[a - min_rating][b - min_rating] += 1
    return conf_mat


def histogram(ratings, min_rating=None, max_rating=None):
    """
    Returns the counts of each type of rating that a rater made
    """
    if min_rating is None:
        min_rating = min(ratings)
    if max_rating is None:
        max_rating = max(ratings)
    num_ratings = int(max_rating - min_rating + 1)
    hist_ratings = [0 for x in range(num_ratings)]
    for r in ratings:
        hist_ratings[r - min_rating] += 1
    return hist_ratings


def quadratic_weighted_kappa(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Calculates the quadratic weighted kappa
    quadratic_weighted_kappa calculates the quadratic weighted kappa
    value, which is a measure of inter-rater agreement between two raters
    that provide discrete numeric ratings.  Potential values range from -1
    (representing complete disagreement) to 1 (representing complete
    agreement).  A kappa value of 0 is expected if all agreement is due to
    chance.
    quadratic_weighted_kappa(rater_a, rater_b), where rater_a and rater_b
    each correspond to a list of integer ratings.  These lists must have the
    same length.
    The ratings should be integers, and it is assumed that they contain
    the complete range of possible ratings.
    quadratic_weighted_kappa(X, min_rating, max_rating), where min_rating
    is the minimum possible rating, and max_rating is the maximum possible
    rating
    """
    rater_a = np.array(rater_a, dtype=int)
    rater_b = np.array(rater_b, dtype=int)
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(min(rater_a), min(rater_b))
    if max_rating is None:
        max_rating = max(max(rater_a), max(rater_b))
    conf_mat = confusion_matrix(rater_a, rater_b,
                                min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    for i in range(num_ratings):
        for j in range(num_ratings):
            expected_count = (hist_rater_a[i] * hist_rater_b[j]
                              / num_scored_items)
            d = pow(i - j, 2.0) / pow(num_ratings - 1, 2.0)
            numerator += d * conf_mat[i][j] / num_scored_items
            denominator += d * expected_count / num_scored_items

    return 1.0 - numerator / denominator


def linear_weighted_kappa(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Calculates the linear weighted kappa
    linear_weighted_kappa calculates the linear weighted kappa
    value, which is a measure of inter-rater agreement between two raters
    that provide discrete numeric ratings.  Potential values range from -1
    (representing complete disagreement) to 1 (representing complete
    agreement).  A kappa value of 0 is expected if all agreement is due to
    chance.
    linear_weighted_kappa(rater_a, rater_b), where rater_a and rater_b
    each correspond to a list of integer ratings.  These lists must have the
    same length.
    The ratings should be integers, and it is assumed that they contain
    the complete range of possible ratings.
    linear_weighted_kappa(X, min_rating, max_rating), where min_rating
    is the minimum possible rating, and max_rating is the maximum possible
    rating
    """
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(rater_a + rater_b)
    if max_rating is None:
        max_rating = max(rater_a + rater_b)
    conf_mat = confusion_matrix(rater_a, rater_b,
                                min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    for i in range(num_ratings):
        for j in range(num_ratings):
            expected_count = (hist_rater_a[i] * hist_rater_b[j]
                              / num_scored_items)
            d = abs(i - j) / float(num_ratings - 1)
            numerator += d * conf_mat[i][j] / num_scored_items
            denominator += d * expected_count / num_scored_items

    return 1.0 - numerator / denominator


def kappa(rater_a, rater_b, min_rating=None, max_rating=None):
    """
    Calculates the kappa
    kappa calculates the kappa
    value, which is a measure of inter-rater agreement between two raters
    that provide discrete numeric ratings.  Potential values range from -1
    (representing complete disagreement) to 1 (representing complete
    agreement).  A kappa value of 0 is expected if all agreement is due to
    chance.
    kappa(rater_a, rater_b), where rater_a and rater_b
    each correspond to a list of integer ratings.  These lists must have the
    same length.
    The ratings should be integers, and it is assumed that they contain
    the complete range of possible ratings.
    kappa(X, min_rating, max_rating), where min_rating
    is the minimum possible rating, and max_rating is the maximum possible
    rating
    """
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
        min_rating = min(rater_a + rater_b)
    if max_rating is None:
        max_rating = max(rater_a + rater_b)
    conf_mat = confusion_matrix(rater_a, rater_b,
                                min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    for i in range(num_ratings):
        for j in range(num_ratings):
            expected_count = (hist_rater_a[i] * hist_rater_b[j]
                              / num_scored_items)
            if i == j:
                d = 0.0
            else:
                d = 1.0
            numerator += d * conf_mat[i][j] / num_scored_items
            denominator += d * expected_count / num_scored_items

    return 1.0 - numerator / denominator


def mean_quadratic_weighted_kappa(kappas, weights=None):
    """
    Calculates the mean of the quadratic
    weighted kappas after applying Fisher's r-to-z transform, which is
    approximately a variance-stabilizing transformation.  This
    transformation is undefined if one of the kappas is 1.0, so all kappa
    values are capped in the range (-0.999, 0.999).  The reverse
    transformation is then applied before returning the result.
    mean_quadratic_weighted_kappa(kappas), where kappas is a vector of
    kappa values
    mean_quadratic_weighted_kappa(kappas, weights), where weights is a vector
    of weights that is the same size as kappas.  Weights are applied in the
    z-space
    """
    kappas = np.array(kappas, dtype=float)
    if weights is None:
        weights = np.ones(np.shape(kappas))
    else:
        weights = weights / np.mean(weights)

    # ensure that kappas are in the range [-.999, .999]
    kappas = np.array([min(x, .999) for x in kappas])
    kappas = np.array([max(x, -.999) for x in kappas])

    z = 0.5 * np.log((1 + kappas) / (1 - kappas)) * weights
    z = np.mean(z)
    return (np.exp(2 * z) - 1) / (np.exp(2 * z) + 1)


def weighted_mean_quadratic_weighted_kappa(solution, submission):
    predicted_score = submission[submission.columns[-1]].copy()
    predicted_score.name = "predicted_score"
    if predicted_score.index[0] == 0:
        predicted_score = predicted_score[:len(solution)]
        predicted_score.index = solution.index
    combined = solution.join(predicted_score, how="left")
    groups = combined.groupby(by="essay_set")
    kappas = [quadratic_weighted_kappa(group[1]["essay_score"], group[1]["predicted_score"]) for group in groups]
    weights = [group[1]["essay_weight"].irow(0) for group in groups]
    return mean_quadratic_weighted_kappa(kappas, weights=weights)


# num_ratings = 5

# def continuous_one_hot(x):
#     columns = []

#     # first rating (0)
#     c0 = T.switch(x < 0, 1, T.switch(x < 1, 1 - (x - 0), 0))
#     columns.append(c0)

#     # middle ratings (1, 2, 3)
#     for r in xrange(1, num_ratings - 1):
#         c = T.switch(x < r  - 1, 0, T.switch(x < r, 1 - (r - x), T.switch(x < r + 1, 1 - (x - r), 0)))
#         columns.append(c)

#     # last rating (4)
#     c4 = T.switch(x < 4 - 1, 0, T.switch(x < 4, 1 - (4 - x), 1))
#     columns.append(c4)

#     return T.stack(columns).T


# def discrete_one_hot(x):
#     x = T.cast(x, 'int32')
#     return T.eye(num_ratings)[x]


# def continuous_conf_mat(rater_a, rater_b):
#     """
#     rater_a: continuous predictions
#     rater_b: labels (integers)
#     """
#     # rater_a_oh = T.eye(num_ratings)[rater_a]
#     rater_a_oh_fractional = continuous_one_hot(rater_a)
#     rater_b_oh = discrete_one_hot(rater_b)
#     conf_mat = T.dot(rater_a_oh_fractional.T, rater_b_oh)
#     return conf_mat


# def discrete_histogram(x):
#     return T.sum(discrete_one_hot(x), axis=0)


# def continuous_histogram(x):
#     return T.sum(continuous_one_hot(x), axis=0)


# def continuous_weighted_kappa(rater_a, rater_b):
#     num_scored_items = rater_a.shape[0]
#     conf_mat = continuous_conf_mat(rater_a, rater_b)

#     hist_rater_a = continuous_histogram(rater_a)
#     hist_rater_b = discrete_histogram(rater_b)

#     expected_counts = T.dot(hist_rater_a[:, None], hist_rater_b[None, :]) / num_scored_items

#     i = T.cast(T.arange(num_ratings), 'float32')
#     j = T.cast(T.arange(num_ratings), 'float32')
#     weight_matrix = (i[:, None] - j[None, :]) ** 2 / (num_ratings - 1) ** 2

#     kappa =  1 - T.sum(weight_matrix * conf_mat) / T.sum(weight_matrix * expected_counts)
#     return kappa

#def minus_kappa(y, t):
#     return -nn_eyes.continuous_weighted_kappa(y[:, 0], t[:, 0])  # turn them back into 1D vectors


# def build_objective(l_in, l_out):
#     return nn.objectives.Objective(l_out, loss_function=minus_kappa)


# def create_train_gen():
#     image_gen = data.gen_images(data.paths_my_train, data.labels_my_train, shuffle=True, repeat=True)

#     def augmented_image_gen():
#         for image, label in image_gen:
#             yield data.augment_image(image, augmentation_params), label

#     chunks_gen = data.gen_chunks(augmented_image_gen(), chunk_size=chunk_size, labels=True)
#     return buffering.buffered_gen_threaded(chunks_gen)



# from data.py
# From the class Paths
	# data_dir = join(getcwd(),'data'))
	# train_dir = join(data_dir,'train')
	# test_dir = train = join(data_dir,'test')
	# train_labels = join(data_dir,'trainLabels.csv')
	# #X_train should be added in data.py
	# #X_valid should be added in data.py
	# #X_test should be added in data.py


# ## The below is from Benanne/Retina

# def gen_images(paths, labels=None, shuffle=False, repeat=False):
#     paths_shuffled = np.array(paths)

#     if labels is not None:
#         labels_shuffled = np.array(labels)

#     while True:
#         if shuffle:
#             state = np.random.get_state()
#             np.random.shuffle(paths_shuffled)
#             if labels is not None:
#                 np.random.set_state(state)
#                 np.random.shuffle(labels_shuffled)

#         for k in xrange(len(paths_shuffled)):
#             path = paths_shuffled[k]
#             im = skimage.io.imread(os.path.join("data", path))
#             im = im.transpose(2, 0, 1).astype('float32') / 255.0

#             if labels is not None:
#                 yield im, labels_shuffled[k]
#             else:
#                 yield im
        
#         if not repeat:
#             break


# def gen_chunks(image_gen, chunk_size=8192, labels=True):
#     chunk = np.zeros((chunk_size, 3, 96, 96), dtype='float32')
    
#     if labels:
#         chunk_labels = np.zeros((chunk_size, 1), dtype='float32')

#     offset = 0

#     for sample in image_gen:
#         if labels:
#             im, label = sample
#         else:
#             im = sample

#         chunk[offset] = im

#         if labels:
#             chunk_labels[offset] = label

#         offset += 1

#         if offset >= chunk_size:
#             if labels:
#                 yield chunk, chunk_labels, offset
#             else:
#                 yield chunk, offset

#             chunk = np.zeros((chunk_size, 3, 96, 96), dtype='float32')

#             if labels:
#                 chunk_labels = np.zeros((chunk_size, 1), dtype='float32')

#             offset = 0

#     if offset > 0:
#         if labels:
#             yield chunk, chunk_labels, offset
#         else:
#             yield chunk, offset


# def fast_warp(img, tf, output_shape=(96, 96), mode='constant'):
#     """
#     This wrapper function is about five times faster than skimage.transform.warp, for our use case.
#     """
#     m = tf.params
#     img_wf = np.empty((3, output_shape[0], output_shape[1]), dtype='float32')
#     for k in xrange(3):
#         img_wf[k] = skimage.transform._warps_cy._warp_fast(img[k], m, output_shape=output_shape, mode=mode)
#     return img_wf


# def build_center_uncenter_transform(image_size):
#     center_shift = np.array(image_size) / 2. - 0.5
#     tform_center = skimage.transform.SimilarityTransform(translation=-center_shift)
#     tform_uncenter = skimage.transform.SimilarityTransform(translation=center_shift)
#     return tform_center, tform_uncenter


# def build_augmentation_transform(zoom=1.0, rotation=0, shear=0, translation=(0, 0), flip=False, image_size=(96, 96)):
#     tform_center, tform_uncenter = build_center_uncenter_transform(image_size)

#     rotation = np.deg2rad(rotation)
#     shear = np.deg2rad(shear)

#     if flip:
#         rotation += 180
#         shear += 180
#         # shear by 180 degrees is equivalent to rotation by 180 degrees + flip.
#         # So after that we rotate it another 180 degrees to get just the flip.

#     tform_augment = skimage.transform.AffineTransform(scale=(1/zoom, 1/zoom), rotation=rotation, shear=shear, translation=translation)
#     tform = tform_center + tform_augment + tform_uncenter # shift to center, augment, shift back (for the rotation/shearing)
#     return tform


# def random_augmentation_transform(zoom_range=(1.0, 1.0), rotation_range=(0, 0), shear_range=(0, 0), 
#                                   translation_range=(0, 0), do_flip=False, image_size=(96, 96)):
#     # random shift
#     shift_x = np.random.uniform(*translation_range)
#     shift_y = np.random.uniform(*translation_range)
#     translation = (shift_x, shift_y)

#     # random rotation
#     rotation = np.random.uniform(*rotation_range)

#     # random shear
#     shear = np.random.uniform(*shear_range)

#     # flip
#     flip = do_flip and (np.random.randint(2) > 0) # flip half of the time

#     # random zoom
#     log_zoom_range = [np.log(z) for z in zoom_range]
#     zoom = np.exp(np.random.uniform(*log_zoom_range))

#     return build_augmentation_transform(zoom, rotation, shear, translation, flip, image_size)


# def augment_image(img, augmentation_params={}):
#     tform_augment = random_augmentation_transform(**augmentation_params)
#     return fast_warp(img, tform_augment, output_shape=(96, 96)).astype('float32')










































# ## The below is from Plankton


# # TODO Consider , but I think I can handle it more effective with dtype and normalization 
# # http://docs.scipy.org/doc/numpy/user/basics.types.html
# # This function is used in chunk_dst below
# def uint_to_float(img):
#     return 1 - (img / np.float32(255.0))



# def extract_image_patch(chunk_dst, img):
#     """
#     extract a correctly sized patch from img and place it into chunk_dst,
#     which assumed to be preinitialized to zeros.
#     """
#     # # DEBUG: draw a border to see where the image ends up
#     # img[0, :] = 127
#     # img[-1, :] = 127
#     # img[:, 0] = 127
#     # img[:, -1] = 127

#     p_x, p_y = chunk_dst.shape
#     im_x, im_y = img.shape

# #  // means unconditionally truncating division
#     offset_x = (im_x - p_x) // 2
#     offset_y = (im_y - p_y) // 2
# # TODO figure where these slice objects are being used. 
#     if offset_x < 0:
#         cx = slice(-offset_x, -offset_x + im_x)
#         ix = slice(0, im_x)
#     else:
#         cx = slice(0, p_x)
#         ix = slice(offset_x, offset_x + p_x)

#     if offset_y < 0:
#         cy = slice(-offset_y, -offset_y + im_y)
#         iy = slice(0, im_y)
#     else:
#         cy = slice(0, p_y)
#         iy = slice(offset_y, offset_y + p_y)

#     chunk_dst[cx, cy] = uint_to_float(img[ix, iy])


# def load(subset='train'):
#     """
#     Load all images into memory for faster processing
#     """
#     return utils.load_gz("data/images_%s.npy.gz" % subset)



# def uint_to_float(img):
#     return 1 - (img / np.float32(255.0))


# def extract_image_patch(chunk_dst, img):
#     """
#     extract a correctly sized patch from img and place it into chunk_dst,
#     which assumed to be preinitialized to zeros.
#     """
#     # # DEBUG: draw a border to see where the image ends up
#     # img[0, :] = 127
#     # img[-1, :] = 127
#     # img[:, 0] = 127
#     # img[:, -1] = 127

#     p_x, p_y = chunk_dst.shape
#     im_x, im_y = img.shape

#     offset_x = (im_x - p_x) // 2
#     offset_y = (im_y - p_y) // 2

#     if offset_x < 0:
#         cx = slice(-offset_x, -offset_x + im_x)
#         ix = slice(0, im_x)
#     else:
#         cx = slice(0, p_x)
#         ix = slice(offset_x, offset_x + p_x)

#     if offset_y < 0:
#         cy = slice(-offset_y, -offset_y + im_y)
#         iy = slice(0, im_y)
#     else:
#         cy = slice(0, p_y)
#         iy = slice(offset_y, offset_y + p_y)

#     chunk_dst[cx, cy] = uint_to_float(img[ix, iy])



# def patches_gen(images, labels, patch_size=(50, 50), chunk_size=4096, num_chunks=100, rng=np.random):
#     p_x, p_y = patch_size

#     for n in xrange(num_chunks):
#         indices = rng.randint(0, len(images), chunk_size)

#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_y = np.zeros((chunk_size,), dtype='float32')

#         for k, idx in enumerate(indices):
#             img = images[indices[k]]
#             extract_image_patch(chunk_x[k], img)
#             chunk_y[k] = labels[indices[k]]
        
#         yield chunk_x, chunk_y


# def patches_gen_ordered(images, patch_size=(50, 50), chunk_size=4096):
#     p_x, p_y = patch_size

#     num_images = len(images)
#     num_chunks = int(np.ceil(num_images / float(chunk_size)))

#     idx = 0

#     for n in xrange(num_chunks):
#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_length = chunk_size

#         for k in xrange(chunk_size):
#             if idx >= num_images:
#                 chunk_length = k
#                 break

#             img = images[idx]
#             extract_image_patch(chunk_x[k], img)
#             idx += 1

#         yield chunk_x, chunk_length


# ## augmentation

# def fast_warp(img, tf, output_shape=(50, 50), mode='constant', order=1):
#     """
#     This wrapper function is faster than skimage.transform.warp
#     """
#     m = tf.params # tf._matrix is
#     return skimage.transform._warps_cy._warp_fast(img, m, output_shape=output_shape, mode=mode, order=order)


# def build_centering_transform(image_shape, target_shape=(50, 50)):
#     rows, cols = image_shape
#     trows, tcols = target_shape
#     shift_x = (cols - tcols) / 2.0
#     shift_y = (rows - trows) / 2.0
#     return skimage.transform.SimilarityTransform(translation=(shift_x, shift_y))


# def build_rescale_transform_slow(downscale_factor, image_shape, target_shape):
#     """
#     This mimics the skimage.transform.resize function.
#     The resulting image is centered.
#     """
#     rows, cols = image_shape
#     trows, tcols = target_shape
#     col_scale = row_scale = downscale_factor
#     src_corners = np.array([[1, 1], [1, rows], [cols, rows]]) - 1
#     dst_corners = np.zeros(src_corners.shape, dtype=np.double)
#     # take into account that 0th pixel is at position (0.5, 0.5)
#     dst_corners[:, 0] = col_scale * (src_corners[:, 0] + 0.5) - 0.5
#     dst_corners[:, 1] = row_scale * (src_corners[:, 1] + 0.5) - 0.5

#     tform_ds = skimage.transform.AffineTransform()
#     tform_ds.estimate(src_corners, dst_corners)

#     # centering    
#     shift_x = cols / (2.0 * downscale_factor) - tcols / 2.0
#     shift_y = rows / (2.0 * downscale_factor) - trows / 2.0
#     tform_shift_ds = skimage.transform.SimilarityTransform(translation=(shift_x, shift_y))
#     return tform_shift_ds + tform_ds


# def build_rescale_transform_fast(downscale_factor, image_shape, target_shape):
#     """
#     estimating the correct rescaling transform is slow, so just use the
#     downscale_factor to define a transform directly. This probably isn't 
#     100% correct, but it shouldn't matter much in practice.
#     """
#     rows, cols = image_shape
#     trows, tcols = target_shape
#     tform_ds = skimage.transform.AffineTransform(scale=(downscale_factor, downscale_factor))
    
#     # centering    
#     shift_x = cols / (2.0 * downscale_factor) - tcols / 2.0
#     shift_y = rows / (2.0 * downscale_factor) - trows / 2.0
#     tform_shift_ds = skimage.transform.SimilarityTransform(translation=(shift_x, shift_y))
#     return tform_shift_ds + tform_ds

# build_rescale_transform = build_rescale_transform_fast


# def build_center_uncenter_transforms(image_shape):
#     """
#     These are used to ensure that zooming and rotation happens around the center of the image.
#     Use these transforms to center and uncenter the image around such a transform.
#     """
#     center_shift = np.array([image_shape[1], image_shape[0]]) / 2.0 - 0.5 # need to swap rows and cols here apparently! confusing!
#     tform_uncenter = skimage.transform.SimilarityTransform(translation=-center_shift)
#     tform_center = skimage.transform.SimilarityTransform(translation=center_shift)
#     return tform_center, tform_uncenter

# def build_augmentation_transform(zoom=(1.0, 1.0), rotation=0, shear=0, translation=(0, 0), flip=False): 
#     if flip:
#         shear += 180
#         rotation += 180
#         # shear by 180 degrees is equivalent to rotation by 180 degrees + flip.
#         # So after that we rotate it another 180 degrees to get just the flip.

#     tform_augment = skimage.transform.AffineTransform(scale=(1/zoom[0], 1/zoom[1]), rotation=np.deg2rad(rotation), shear=np.deg2rad(shear), translation=translation)
#     return tform_augment

# def random_perturbation_transform(zoom_range, rotation_range, shear_range, translation_range, do_flip=True, allow_stretch=False, rng=np.random):
#     shift_x = rng.uniform(*translation_range)
#     shift_y = rng.uniform(*translation_range)
#     translation = (shift_x, shift_y)

#     rotation = rng.uniform(*rotation_range)
#     shear = rng.uniform(*shear_range)

#     if do_flip:
#         flip = (rng.randint(2) > 0) # flip half of the time
#     else:
#         flip = False

#     # random zoom
#     log_zoom_range = [np.log(z) for z in zoom_range]
#     if isinstance(allow_stretch, float):
#         log_stretch_range = [-np.log(allow_stretch), np.log(allow_stretch)]
#         zoom = np.exp(rng.uniform(*log_zoom_range))
#         stretch = np.exp(rng.uniform(*log_stretch_range))
#         zoom_x = zoom * stretch
#         zoom_y = zoom / stretch
#     elif allow_stretch is True: # avoid bugs, f.e. when it is an integer
#         zoom_x = np.exp(rng.uniform(*log_zoom_range))
#         zoom_y = np.exp(rng.uniform(*log_zoom_range))
#     else:
#         zoom_x = zoom_y = np.exp(rng.uniform(*log_zoom_range))
#     # the range should be multiplicatively symmetric, so [1/1.1, 1.1] instead of [0.9, 1.1] makes more sense.

#     return build_augmentation_transform((zoom_x, zoom_y), rotation, shear, translation, flip)

# def perturb(img, augmentation_params, target_shape=(50, 50), rng=np.random):
#     # # DEBUG: draw a border to see where the image ends up
#     # img[0, :] = 0.5
#     # img[-1, :] = 0.5
#     # img[:, 0] = 0.5
#     # img[:, -1] = 0.5
#     tform_centering = build_centering_transform(img.shape, target_shape)
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = random_perturbation_transform(rng=rng, **augmentation_params)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)
#     return fast_warp(img, tform_centering + tform_augment, output_shape=target_shape, mode='constant').astype('float32')



# def patches_gen_augmented(images, labels, patch_size=(50, 50), chunk_size=4096,
#         num_chunks=100, rng=np.random, rng_aug=np.random, augmentation_params=default_augmentation_params):
#     p_x, p_y = patch_size

#     if augmentation_params is None:
#         augmentation_params = no_augmentation_params

#     for n in xrange(num_chunks):
#         indices = rng.randint(0, len(images), chunk_size)

#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_y = labels[indices].astype('float32')

#         for k, idx in enumerate(indices):
#             img = images[idx]
#             img = uint_to_float(img)
#             chunk_x[k] = perturb(img, augmentation_params, target_shape=patch_size, rng=rng_aug)
        
#         yield chunk_x, chunk_y


# ## RESCALING


# def perturb_rescaled(img, scale, augmentation_params, target_shape=(50, 50), rng=np.random):
#     """
#     scale is a DOWNSCALING factor.
#     """
#     tform_rescale = build_rescale_transform(scale, img.shape, target_shape) # also does centering
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = random_perturbation_transform(rng=rng, **augmentation_params)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)
#     return fast_warp(img, tform_rescale + tform_augment, output_shape=target_shape, mode='constant').astype('float32')


# def rescaled_patches_gen_augmented(images, labels, estimate_scale_func, patch_size=(50, 50),
#         chunk_size=4096, num_chunks=100, rng=np.random, rng_aug=np.random, augmentation_params=default_augmentation_params):
#     p_x, p_y = patch_size

#     if augmentation_params is None:
#         augmentation_params = no_augmentation_params

#     for n in xrange(num_chunks):
#         indices = rng.randint(0, len(images), chunk_size)

#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_y = labels[indices].astype('float32')
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')

#         for k, idx in enumerate(indices):
#             img = images[idx]
#             img = uint_to_float(img)
#             scale = estimate_scale_func(img)
#             chunk_x[k] = perturb_rescaled(img, scale, augmentation_params, target_shape=patch_size, rng=rng_aug)
#             chunk_shape[k] = img.shape
        
#         yield chunk_x, chunk_y, chunk_shape


# def rescaled_patches_gen_ordered(images, estimate_scale_func, patch_size=(50, 50), chunk_size=4096,
#         augmentation_params=no_augmentation_params, rng=np.random, rng_aug=np.random):
#     p_x, p_y = patch_size

#     num_images = len(images)
#     num_chunks = int(np.ceil(num_images / float(chunk_size)))

#     idx = 0

#     for n in xrange(num_chunks):
#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')
#         chunk_length = chunk_size

#         for k in xrange(chunk_size):
#             if idx >= num_images:
#                 chunk_length = k
#                 break

#             img = images[idx]
#             img = uint_to_float(img)
#             scale = estimate_scale_func(img)
#             chunk_x[k] = perturb_rescaled(img, scale, augmentation_params, target_shape=patch_size, rng=rng_aug)
#             chunk_shape[k] = img.shape
#             idx += 1

#         yield chunk_x, chunk_shape, chunk_length


# # for test-time augmentation
# def perturb_rescaled_fixed(img, scale, tform_augment, target_shape=(50, 50)):
#     """
#     scale is a DOWNSCALING factor.
#     """
#     tform_rescale = build_rescale_transform(scale, img.shape, target_shape) # also does centering
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)
#     return fast_warp(img, tform_rescale + tform_augment, output_shape=target_shape, mode='constant').astype('float32')


# def rescaled_patches_gen_fixed(images, estimate_scale_func, patch_size=(50, 50), chunk_size=4096,
#         augmentation_transforms=None, rng=np.random):
#     if augmentation_transforms is None:
#         augmentation_transforms = [tform_identity]

#     p_x, p_y = patch_size

#     num_images = len(images)
#     num_tfs = len(augmentation_transforms)
#     num_patches = num_images * num_tfs
#     num_chunks = int(np.ceil(num_patches / float(chunk_size)))

#     idx = 0

#     for n in xrange(num_chunks):
#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')
#         chunk_length = chunk_size

#         for k in xrange(chunk_size):
#             if idx >= num_patches:
#                 chunk_length = k
#                 break

#             img = images[idx // num_tfs]
#             img = uint_to_float(img)
#             tf = augmentation_transforms[idx % num_tfs]
#             scale = estimate_scale_func(img) # could technically be cached but w/e
#             chunk_x[k] = perturb_rescaled_fixed(img, scale, tf, target_shape=patch_size)
#             chunk_shape[k] = img.shape
#             idx += 1

#         yield chunk_x, chunk_shape, chunk_length



# ### MULTISCALE GENERATORS

# def perturb_multiscale(img, scale_factors, augmentation_params, target_shapes, rng=np.random):
#     """
#     scale is a DOWNSCALING factor.
#     """
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = random_perturbation_transform(rng=rng, **augmentation_params)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)

#     output = []
#     for scale, target_shape in zip(scale_factors, target_shapes):
#         if isinstance(scale, skimage.transform.ProjectiveTransform):
#             tform_rescale = scale
#         else:
#             tform_rescale = build_rescale_transform(scale, img.shape, target_shape) # also does centering
#         output.append(fast_warp(img, tform_rescale + tform_augment, output_shape=target_shape, mode='constant').astype('float32'))

#     return output


# def multiscale_patches_gen_augmented(images, labels, scale_factors=[1.0], patch_sizes=[(50, 50)],
#         chunk_size=4096, num_chunks=100, rng=np.random, rng_aug=np.random, augmentation_params=default_augmentation_params):
#     assert len(patch_sizes) == len(scale_factors)
#     if augmentation_params is None:
#         augmentation_params = no_augmentation_params

#     for n in xrange(num_chunks):
#         indices = rng.randint(0, len(images), chunk_size)

#         chunks_x = [np.zeros((chunk_size, p_x, p_y), dtype='float32') for p_x, p_y in patch_sizes]
#         chunk_y = labels[indices].astype('float32')
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')

#         for k, idx in enumerate(indices):
#             img = images[idx]
#             img = uint_to_float(img)
#             sfs = [(sf(img) if callable(sf) else sf) for sf in scale_factors] # support both fixed scale factors and variable scale factors with callables
#             patches = perturb_multiscale(img, sfs, augmentation_params, target_shapes=patch_sizes, rng=rng_aug)
#             for chunk_x, patch in zip(chunks_x, patches):
#                 chunk_x[k] = patch

#             chunk_shape[k] = img.shape
        
#         yield chunks_x, chunk_y, chunk_shape


# # for test-time augmentation
# def perturb_multiscale_fixed(img, scale_factors, tform_augment, target_shapes):
#     """
#     scale is a DOWNSCALING factor.
#     """
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)

#     output = []
#     for scale, target_shape in zip(scale_factors, target_shapes):
#         if isinstance(scale, skimage.transform.ProjectiveTransform):
#             tform_rescale = scale
#         else:
#             tform_rescale = build_rescale_transform(scale, img.shape, target_shape) # also does centering
#         output.append(fast_warp(img, tform_rescale + tform_augment, output_shape=target_shape, mode='constant').astype('float32'))

#     return output


# def multiscale_patches_gen_fixed(images, scale_factors=[1.0], patch_sizes=[(50, 50)], chunk_size=4096,
#         augmentation_transforms=None, rng=np.random):
#     if augmentation_transforms is None:
#         augmentation_transforms = [tform_identity]

#     assert len(patch_sizes) == len(scale_factors)

#     num_images = len(images)
#     num_tfs = len(augmentation_transforms)
#     num_patches = num_images * num_tfs
#     num_chunks = int(np.ceil(num_patches / float(chunk_size)))

#     idx = 0

#     for n in xrange(num_chunks):
#         chunks_x = [np.zeros((chunk_size, p_x, p_y), dtype='float32') for p_x, p_y in patch_sizes]
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')
#         chunk_length = chunk_size

#         for k in xrange(chunk_size):
#             if idx >= num_patches:
#                 chunk_length = k
#                 break

#             img = images[idx // num_tfs]
#             img = uint_to_float(img)
#             tf = augmentation_transforms[idx % num_tfs]

#             sfs = [(sf(img) if callable(sf) else sf) for sf in scale_factors] # support both fixed scale factors and variable scale factors with callables
#             patches = perturb_multiscale_fixed(img, sfs, tf, target_shapes=patch_sizes)
#             for chunk_x, patch in zip(chunks_x, patches):
#                 chunk_x[k] = patch

#             chunk_shape[k] = img.shape
#             idx += 1

#         yield chunks_x, chunk_shape, chunk_length




# def intensity_jitter(chunk, std=0.1, rng=np.random):
#     factors = np.exp(rng.normal(0.0, std, chunk.shape[0])).astype(chunk.dtype)
#     return chunk * factors[:, None, None]



# ### GAUSSIAN AUGMENTATION PARAMETER DISTRIBUTIONS


# def random_perturbation_transform_gaussian(zoom_std, rotation_range, shear_std, translation_std, do_flip=True, stretch_std=0.0, rng=np.random):
#     shift_x = rng.normal(0.0, translation_std)
#     shift_y = rng.normal(0.0, translation_std)
#     translation = (shift_x, shift_y)

#     rotation = rng.uniform(*rotation_range)
#     shear = rng.normal(0.0, shear_std)

#     if do_flip:
#         flip = (rng.randint(2) > 0) # flip half of the time
#     else:
#         flip = False

#     zoom = np.exp(rng.normal(0.0, zoom_std))
#     stretch = np.exp(rng.normal(0.0, stretch_std))
#     zoom_x = zoom * stretch
#     zoom_y = zoom / stretch

#     return build_augmentation_transform((zoom_x, zoom_y), rotation, shear, translation, flip)


# def perturb_rescaled_gaussian(img, scale, augmentation_params, target_shape=(50, 50), rng=np.random):
#     """
#     scale is a DOWNSCALING factor.
#     """
#     tform_rescale = build_rescale_transform(scale, img.shape, target_shape) # also does centering
#     tform_center, tform_uncenter = build_center_uncenter_transforms(img.shape)
#     tform_augment = random_perturbation_transform_gaussian(rng=rng, **augmentation_params)
#     tform_augment = tform_uncenter + tform_augment + tform_center # shift to center, augment, shift back (for the rotation/shearing)
#     return fast_warp(img, tform_rescale + tform_augment, output_shape=target_shape, mode='constant').astype('float32')


# def rescaled_patches_gen_augmented_gaussian(images, labels, estimate_scale_func, patch_size=(50, 50),
#         chunk_size=4096, num_chunks=100, rng=np.random, rng_aug=np.random, augmentation_params=None):
#     p_x, p_y = patch_size

#     if augmentation_params is None:
#         augmentation_params = no_augmentation_params_gaussian

#     for n in xrange(num_chunks):
#         indices = rng.randint(0, len(images), chunk_size)

#         chunk_x = np.zeros((chunk_size, p_x, p_y), dtype='float32')
#         chunk_y = labels[indices].astype('float32')
#         chunk_shape = np.zeros((chunk_size, 2), dtype='float32')

#         for k, idx in enumerate(indices):
#             img = images[idx]
#             img = uint_to_float(img)
#             scale = estimate_scale_func(img)
#             chunk_x[k] = perturb_rescaled_gaussian(img, scale, augmentation_params, target_shape=patch_size, rng=rng_aug)
#             chunk_shape[k] = img.shape
        
#         yield chunk_x, chunk_y, chunk_shape



