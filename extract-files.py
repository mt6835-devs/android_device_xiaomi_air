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
    'system_ext/lib64/libsink.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    ('system_ext/etc/init/init.vtservice.rc', 'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'): blob_fixup()
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
        ),
    'vendor/lib64/hw/hwcomposer.mtk_common.so' : blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/librgbwlightsensor.so',
        'vendor/lib64/mt6835/libaalservice.so',
        'vendor/lib64/mt6835/libcam.utils.sensorprovider.so'    
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
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
