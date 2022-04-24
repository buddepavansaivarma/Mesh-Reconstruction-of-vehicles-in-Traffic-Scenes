from collections import OrderedDict

import cv2
import numpy as np
import yaml

from utils.geometry import pascal_vpoint_to_extrinsics, intrinsic_matrix

pascal_classes_to_COCO = {
    'aeroplane': [4],
    'bicycle': [1],
    'boat': [8],
    'bottle': [39],
    'bus': [5],
    'car': [2, 7],
    'chair': [56],
    'diningtable': [60],
    'motorbike': [3],
    'sofa': [57],
    'train': [6],
    'tvmonitor': [62]
}


class CustomDumper(yaml.Dumper):
    # Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
    def represent_dict_preserve_order(self, data):
        return self.represent_dict(data.items())


def process_annotations(dataset_dir, results_dir):
    for pascal_class, COCO_ids in pascal_classes_to_COCO.items():
        result_dir = results_dir / f'{pascal_class}'
        for sub_dir in ['images', 'annotations']:
            curr_dir = result_dir / sub_dir
            if not curr_dir.is_dir():
                curr_dir.mkdir(parents=True, exist_ok=True)

        with open(str(dataset_dir / 'annotations' / f'pascal3d_{pascal_class}_keypoints.txt'), 'r') as fp:
            pascal_annotations = fp.readlines()
            for i, line in enumerate(pascal_annotations):
                line = line.replace('\n', '')
                pascal_annotations[i] = line.split(',')

        with open(str(dataset_dir / 'annotations' / f'pascal3d_{pascal_class}_difficulty.txt'), 'r') as fp:
            pascal_difficulty_annotations = fp.readlines()
            for i, line in enumerate(pascal_difficulty_annotations):
                line = line.replace('\n', '')
                pascal_difficulty_annotations[i] = line.split(',')
            pascal_difficulty_annotations = np.asarray(pascal_difficulty_annotations)

        CustomDumper.add_representer(OrderedDict, CustomDumper.represent_dict_preserve_order)

        for n, annot in enumerate(pascal_annotations):
            img = cv2.imread(str(dataset_dir / 'images' / f'{pascal_class}_{annot[1]}' / annot[2]))

            # object CAD
            cad_id = int(annot[6]) - 1

            # object bbox
            bbox = [int(annot[7]), int(annot[8]), int(annot[9]), int(annot[10])]
            if bbox[0] < 0:
                bbox[0] = 0
            if bbox[1] < 0:
                bbox[1] = 0
            if bbox[2] >= img.shape[1]:
                bbox[2] = img.shape[1] - 1
            if bbox[3] >= img.shape[0]:
                bbox[3] = img.shape[0] - 1

            # object pose
            az = float(annot[11])
            el = float(annot[12])
            # theta = float(annot[13])
            rad = float(annot[14])
            cx, cy = float(annot[19]), float(annot[20])

            # object occlusion
            occluded = int(annot[25])
            truncated = int(annot[26])
            difficult = int(pascal_difficulty_annotations[n, 1])

            # Keypoints
            num_kps = (len(annot) - 27) // 3
            kpoint_idxs = np.arange(27, len(annot)).reshape(num_kps, 3)
            kpoints = np.zeros((num_kps, 3), dtype=int)  # x, y, visibility (0=not visible, 1=visible)

            for k, idxs in enumerate(kpoint_idxs):
                kpoints[k, 0] = int(annot[idxs[1]])
                kpoints[k, 1] = int(annot[idxs[2]])
                if int(annot[idxs[0]]) == 1:
                    kpoints[k, 2] = 1
                else:
                    kpoints[k, 2] = 0

            if len(list((result_dir / 'images').glob(annot[2]))) == 0:
                cv2.imwrite(str(result_dir / 'images' / annot[2]), img)

            # compute correct intrinsic and extrinsic matrices
            K = intrinsic_matrix(fx=3000, fy=3000, cx=cx, cy=cy)
            extrinsic = pascal_vpoint_to_extrinsics(az_deg=az, el_deg=el, radius=rad)

            # create annotation file
            new_annot = OrderedDict()
            new_annot['image_name'] = annot[2]
            new_annot['image_size'] = [img.shape[0], img.shape[1], img.shape[2]]
            new_annot['pascal_class'] = pascal_class
            new_annot['cad_idx'] = cad_id
            new_annot['occluded'] = occluded
            new_annot['truncated'] = truncated
            new_annot['difficult'] = difficult
            new_annot['bbox'] = bbox
            new_annot['kpoints_2d'] = [[int(kp[0]), int(kp[1]), int(kp[2])] for kp in kpoints]
            new_annot['intrinsic'] = [[float(val[i]) for i in range(len(val))] for val in K]
            new_annot['extrinsic'] = [[float(val[i]) for i in range(len(val))] for val in extrinsic]

            with open(str(result_dir / 'annotations' / f'{n:05}.yaml'), 'w') as fp:
                yaml.dump(new_annot, fp, Dumper=CustomDumper)
