#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import re

from extract_utils.file import File
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/air',
    'hardware/mediatek',
    'hardware/mediatek/libaedv',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libneuron_graph_delegate.mtk',
        'libtflite_mtk',
        'vendor.mediatek.hardware.apuware.utils@2.0',
        'vendor.mediatek.hardware.videotelephony@1.0'
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/hw/android.hardware.security.keymint@2.0-service.mitee': blob_fixup()
        .replace_needed('android.hardware.security.keymint-V2-ndk.so', 'android.hardware.security.keymint-V3-ndk.so')
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    (
        'system_ext/lib64/libmtk_vt_service.so',
        'system_ext/lib64/libmtk_vt_wrapper.so',
        'system_ext/lib/libmtk_vt_wrapper.so',
    ): blob_fixup()
        .replace_needed('libhidltransport.so', 'libhidlbase.so'),
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .binary_regex_replace(
            re.escape(b'\xb3F\x04\xb9\x08\x00@\xf9\x08-@\xf9\x00\x01?\xd6'),
            b'\xb3F\x04\xb9\x08\x00@\xf9\x089@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b'\xe1\x03\x08*)-@\xf9 \x01?\xd6\x04\x00\x00\x14\x08\x00@\xf9\x08-@\xf9\x00\x01?\xd6\x80\x16@\xf9!\x00\xa0R\x08\x00@\xf9\x08E@\xf9\x00\x01?\xd6'),
            b'\xe1\x03\x08*)9@\xf9 \x01?\xd6\x04\x00\x00\x14\x08\x00@\xf9\x089@\xf9\x00\x01?\xd6\x80\x16@\xf9!\x00\xa0R\x08\x00@\xf9\x08Y@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b'\x08\x00@\xf9\x08=@\xf9\x00\x01?\xd6\x80\x16@\xf9A\x18\xa1R\x08\x00@\xf9\x08A@\xf9\x00\x01?\xd6A\xff\xff\xf0!\xe4\x1f\x91\xe0\x83\x00\x91\x95\x16@\xf98\x0c\x00\x94\xa8\x02@\xf9\xe1\x83\x00\x91\xe0\x03\x15\xaa\x089@\xf9\x00\x01?\xd6'),
            b'\x08\x00@\xf9\x08Q@\xf9\x00\x01?\xd6\x80\x16@\xf9A\x18\xa1R\x08\x00@\xf9\x08U@\xf9\x00\x01?\xd6A\xff\xff\xf0!\xe4\x1f\x91\xe0\x83\x00\x91\x95\x16@\xf98\x0c\x00\x94\xa8\x02@\xf9\xe1\x83\x00\x91\xe0\x03\x15\xaa\x08M@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b'\xe2\x03\x1f*\x08!@\xf9\x00\x01?\xd6'),
            b'\xe2\x03\x1f*\x08)@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b'\x08\x00@\xf9\x085@\xf9\x00\x01?\xd6'),
            b'\x08\x00@\xf9\x08E@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b't\xc2\x13\x91\x08\x00@\xf9\x08\x1d@\xf9%\x00\x00\xf0'),
            b't\xc2\x13\x91\x08\x00@\xf9\x08%@\xf9%\x00\x00\xf0',
        )
        .binary_regex_replace(
            re.escape(b'`\x16@\xf9\x08\x00@\xf9\x08%@\xf9\x00\x01?\xd6\xf4\x03\x00*'),
            b'`\x16@\xf9\x08\x00@\xf9\x08-@\xf9\x00\x01?\xd6\xf4\x03\x00*',
        )
        .binary_regex_replace(
            re.escape(b'\x82\xc6B\xf9\x08\x00@\xf9\x08\x1d@\xf9%\x00\x00\xf0'),
            b'\x82\xc6B\xf9\x08\x00@\xf9\x08%@\xf9%\x00\x00\xf0',
        )
        .binary_regex_replace(
            re.escape(b'\xe3\x03\x1f\xaa\x08\x00@\xf9\x08\x11@\xf9\x00\x01?\xd6'),
            b'\xe3\x03\x1f\xaa\x08\x00@\xf9\x08\x19@\xf9\x00\x01?\xd6',
        )
        .binary_regex_replace(
            re.escape(b'h\x05\x00\x94\xe5\xe3@\xb9\xbf\x00\x01q\xc2\x11\x00T\xf8#@\xf9X\x02\x00\xb4|\x12\x05\x8b\xf6\x03\x1a\xaa\xe0\x03\x18\xaa\x9a\x0fC\xf8\xe1\x03\x1c\xaa}\x05\x00\x94\x9a\x00\x00\xb4\xe0\x03\x1a\xaa\xe1\x03\x1c\xaa]\x05\x00\x94\x88\x03@\xf9_\x03\x08\xeb@\x00\x00T]\x05\x00\x94\xe5\xe3@\xb9\xfa\x03\x16\xaa\x98\x03\x00\xf9\xe8o@\xf9i\xd2%\x8b'),
            b'h\x05\x00\x94\xe5\xf3@\xb9\xbf\x00\x01q\xc2\x11\x00T\xf8#@\xf9X\x02\x00\xb4|\x12\x05\x8b\xf6\x03\x1a\xaa\xe0\x03\x18\xaa\x9a\x0fC\xf8\xe1\x03\x1c\xaa}\x05\x00\x94\x9a\x00\x00\xb4\xe0\x03\x1a\xaa\xe1\x03\x1c\xaa]\x05\x00\x94\x88\x03@\xf9_\x03\x08\xeb@\x00\x00T]\x05\x00\x94\xe5\xf3@\xb9\xfa\x03\x16\xaa\x98\x03\x00\xf9\xe8w@\xf9i\xd2%\x8b',
        )
        .binary_regex_replace(
            re.escape(b'\xe3\x03\x1f\xaa\xe1\xe3@\xb9\xe4\x03\x1f\xaa\xe2o@\xf9\x08\x00@\xf9\x08\x1d@\xf9%\x00\x00\xd0\xa5\x98E\xf9\x00\x01?\xd6\x98\xff\xff\x17T\x01\x80\x12R\x00\x00\x14h\xc2D\xb9i\xf2R9\x08\x05\x00\x11h\xc2\x04\xb9\xe9\x04\x004\xe1\xe3@\xb9\xf5#@\xf9aJ\x04\xb95\x02\x00\xb4(|@\x93\xe0\x03\x15\xaav\x12\x08\x8b\xd7\x0eC\xf8\xe1\x03\x16\xaa,\x05\x00\x94\x97\x00\x00\xb4\xe0\x03\x17\xaa\xe1\x03\x16\xaa\x0c\x05\x00\x94\xc8\x02@\xf9\xff\x02\x08\xeb@\x00\x00T\x0c\x05\x00\x94\xe1\xe3@\xb9\xd5\x02\x00\xf9h\xc2\x00\x91\xe2o@\xf9\t\xd1!\x8b'),
            b'\xe3\x03\x1f\xaa\xe1\xf3@\xb9\xe4\x03\x1f\xaa\xe2w@\xf9\x08\x00@\xf9\x08%@\xf9%\x00\x00\xd0\xa5\x98E\xf9\x00\x01?\xd6\x98\xff\xff\x17T\x01\x80\x12R\x00\x00\x14h\xc2D\xb9i\xf2R9\x08\x05\x00\x11h\xc2\x04\xb9\xe9\x04\x004\xe1\xf3@\xb9\xf5#@\xf9aJ\x04\xb95\x02\x00\xb4(|@\x93\xe0\x03\x15\xaav\x12\x08\x8b\xd7\x0eC\xf8\xe1\x03\x16\xaa,\x05\x00\x94\x97\x00\x00\xb4\xe0\x03\x17\xaa\xe1\x03\x16\xaa\x0c\x05\x00\x94\xc8\x02@\xf9\xff\x02\x08\xeb@\x00\x00T\x0c\x05\x00\x94\xe1\xf3@\xb9\xd5\x02\x00\xf9h\xc2\x00\x91\xe2w@\xf9\t\xd1!\x8b',
        )
        .binary_regex_replace(
            re.escape(b'\x1f\x01\t\xeb\x01!\x00T\xe0\x03\x14*'),
            b'\x1f\x01\t\xeb\x1f \x03\xd5\xe0\x03\x14*',
        )
        .binary_regex_replace(
            re.escape(b'\xe4\x03\x1f\xaa\x08\x00@\xf9\x08\x1d@\xf9%\x00\x00\xd0'),
            b'\xe4\x03\x1f\xaa\x08\x00@\xf9\x08%@\xf9%\x00\x00\xd0',
        )
        .binary_regex_replace(
            re.escape(b'\t\x00@\xf9\x02\x1d@\xf9(\x1d@\xf9%\x00\x00\xb0'),
            b'\t\x00@\xf9\x02\x1d@\xf9(%@\xf9%\x00\x00\xb0',
        ),
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/bin/hw/android.hardware.graphics.composer@3.1-service': blob_fixup()
        .replace_needed('android.hardware.graphics.composer@2.1-resources.so', 'android.hardware.graphics.composer@2.1-resources-v34.so'),
    (
        'vendor/bin/hw/android.hardware.neuralnetworks-shim-service-mtk',
        'vendor/lib64/libtflite_mtk.so',
        'vendor/lib64/libnvram.so',
        'vendor/lib64/libsysenv.so'
    ): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    'vendor/lib64/hw/audio.primary.mt6835.so': blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-stock.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
        .binary_regex_replace(b'A2dpsuspendonly', b'A2dpSuspended\x00\x00')
        .binary_regex_replace(b'BTAudiosuspend', b'A2dpSuspended\x00')
        .binary_regex_replace(
            re.escape(b'\x9f\x00\x13\x6b\x41\x01\x00\x54\x41\xf3\xff\xf0\xa2\xf3\xff\xd0\xc3\xf1\xff\xf0\x21\x20\x21\x91\x42\x60\x3f\x91\x63\x98\x04\x91\xa0\x00\x80\x52\xe4\x03\x13\x2a\x0a\x00\x00\x14'),
            b'\x7f\x0a\x00\x71\xc0\x00\x00\x54\x7f\x12\x00\x71\x80\x00\x00\x54\xb3\x00\x00\x35\x9f\x76\x06\x39\x03\x00\x00\x14\x28\x00\x80\x52\x88\x76\x06\x39\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\x1f\x01\x10\x71\x01\x02\x00\x54\x00\x8f\x80\x52\x2b\x25\x01\x94\xf6\x03\x00\xaa\xe1\x03\x15\xaa\x14\x36\x01\x94\xf8\x00\x00\x14'),
            b'\x69\x96\x41\xb9\xe9\x00\x00\x34\x0f\x00\x00\x14\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\xc8\x76\x46\x39\x28\x21\x00\x34'),
            b'\xc8\x96\x41\xb9\x28\x21\x00\x34',
        )
        .binary_regex_replace(
            re.escape(b'\x86\x76\x46\x39\xd5\x12\x00\x34'),
            b'\x86\x96\x41\xb9\xd5\x12\x00\x34',
        )
        .binary_regex_replace(
            re.escape(b'\x6b\x03\x01\x94\x88\x76\x46\x39'),
            b'\x6b\x03\x01\x94\x88\x96\x41\xb9',
        )
        .binary_regex_replace(
            re.escape(b'\xde\xf7\x00\x94\x88\x76\x46\x39'),
            b'\xde\xf7\x00\x94\x88\x96\x41\xb9',
        )
        .binary_regex_replace(
            re.escape(b'\xfd\x7b\xbe\xa9\xf3\x0b\x00\xf9\xfd\x03\x00\x91\x31\x07\x00\x94'),
            b'\x00\x00\x80\x52\xc0\x03\x5f\xd6\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\x48\x01\x00\xd0\x00\x01\x6b\x39\xc0\x03\x5f\xd6'),
            b'\x00\x00\x80\x52\xc0\x03\x5f\xd6\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\x88\x66\x03\x94\x80\x02\x00\x36'),
            b'\x88\x66\x03\x94\x14\x00\x00\x14',
        )
        .binary_regex_replace(
            re.escape(b'\x00\x90\x22\x1e\x80\xc2\x40\xf9\x00\x09\x20\x1e\x09\x00\x40\xf9\x08\x00\x38\x1e\x01\x05\x00\x11\x28\x21\x40\xf9\x00\x01\x3f\xd6'),
            b'\x00\xd0\x24\x1e\x80\xc2\x40\xf9\x00\x09\x20\x1e\x09\x00\x40\xf9\x01\x00\x24\x1e\x1f\x20\x03\xd5\x28\x21\x40\xf9\x00\x01\x3f\xd6',
        )
        .binary_regex_replace(
            re.escape(b'\x88\x66\x40\xf9\x88\x03\x00\xb4\x88\x62\x40\xf9\x00\x05\x40\xf9\x08\x00\x40\xf9\x08\x8d\x40\xf9\x00\x01\x3f\xd6\x15\x2c\x40\xb9\x16\x00\x00\x14'),
            b'\x95\x4a\x42\xb9\x55\x00\x00\x35\x95\x4e\x42\xb9\x1b\x00\x00\x14\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\xfd\x7b\xbd\xa9\xf5\x0b\x00\xf9\xfd\x03\x00\x91\xf4\x4f\x02\xa9\x73\xf0\xff\xd0\x35\x01\x00\xf0'),
            b'\x20\x00\x80\x52\xc0\x03\x5f\xd6\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        )
        .binary_regex_replace(
            re.escape(b'\x6a\x49\x34\x8b\x29\x01\x0a\x8b\x28\x01\x08\x8b\x01\x85\x40\x39'),
            b'\x61\x02\x80\x52\x21\x00\x14\x6b\x08\x01\x80\x52\x01\xb1\x81\x1a',
        ),
    'vendor/lib64/hw/hwcomposer.mtk_common.so' : blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/librgbwlightsensor.so',
        'vendor/lib64/mt6835/libaalservice.so',
        'vendor/lib64/mt6835/libcam.utils.sensorprovider.so'
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('libmnl.so', 'libmnl-v33.so'),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    'vendor/lib/libvcodec_oal.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    (
        'vendor/lib64/hw/mt6835/vendor.mediatek.hardware.pq_aidl-impl.so',
        'vendor/lib64/librt_extamp_intf.so',
        'vendor/lib64/libpqxmlparser.so'
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/lib64/mt6835/libneuralnetworks_sl_driver_mtk_prebuilt.so', 
        'vendor/lib64/libTrueSight.so', 
        'vendor/lib64/libMiVideoFilter.so'
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_acquire')
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle'),
    'vendor/lib64/mt6835/lib3a.ae.stat.so': blob_fixup()
        .add_needed('liblog.so'),
    (
        'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
        'vendor/lib64/libcodec2_vpp_AISR_plugin.so'
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/libgoodixhwfingerprint.so': blob_fixup()
        .patchelf_version('0_17_2')
        .replace_needed(
            "libvendor.goodix.hardware.biometrics.fingerprint@2.1.so",
            "vendor.goodix.hardware.biometrics.fingerprint@2.1.so"
        ),
    ('vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed('libformatter.so', 'libformatter-v33.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'air',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
