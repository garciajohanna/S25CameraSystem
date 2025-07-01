package galaxy.camera

import android.Manifest
import android.app.ActivityManager
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.camera2.*
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import java.time.LocalDateTime

class MainActivity : ComponentActivity() {

    private val createFileLauncher = registerForActivityResult(
        ActivityResultContracts.CreateDocument("text/markdown")
    ) { uri: Uri? ->
        uri?.let {
            saveHdrAndMemoryInfoToMarkdown(it)
        } ?: run {
            Toast.makeText(this, "File creation cancelled", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(arrayOf(Manifest.permission.CAMERA), 0)
        } else {
            promptUserToSaveMarkdown()
        }
    }

    private fun promptUserToSaveMarkdown() {
        createFileLauncher.launch("camera_hdr_memory_log.md")
    }

    private fun saveHdrAndMemoryInfoToMarkdown(uri: Uri) {
        val cameraManager = getSystemService(Context.CAMERA_SERVICE) as CameraManager
        val builder = StringBuilder()

        for (cameraId in cameraManager.cameraIdList) {
            val characteristics = cameraManager.getCameraCharacteristics(cameraId)

            builder.appendLine("\n## Camera ID: `$cameraId`")

            // Moto G identification (optional)
            val deviceModel = Build.MODEL
            builder.appendLine("### Device: $deviceModel")

            // HDR Profiles (API 33+ only)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                val profiles = characteristics.get(CameraCharacteristics.REQUEST_AVAILABLE_DYNAMIC_RANGE_PROFILES)
                if (profiles != null) {
                    builder.appendLine("\n### Supported HDR Profiles")
                    for (profile in profiles.supportedProfiles) {
                        val constraints = profiles.getProfileCaptureRequestConstraints(profile)
                        builder.appendLine("- $profile: $constraints")
                    }
                } else {
                    builder.appendLine("\n_No HDR profiles found._")
                }
            }

            // General characteristics
            val aeModes = characteristics.get(CameraCharacteristics.CONTROL_AE_AVAILABLE_MODES)
            builder.appendLine("\n### AE Modes\n`${aeModes?.contentToString()}`")

            val sceneModes = characteristics.get(CameraCharacteristics.CONTROL_AVAILABLE_SCENE_MODES)
            builder.appendLine("\n### Scene Modes\n`${sceneModes?.contentToString()}`")

            val tonemapModes = characteristics.get(CameraCharacteristics.TONEMAP_AVAILABLE_TONE_MAP_MODES)
            builder.appendLine("\n### Tonemap Modes\n`${tonemapModes?.contentToString()}`")

            val fpsRanges = characteristics.get(CameraCharacteristics.CONTROL_AE_AVAILABLE_TARGET_FPS_RANGES)
            builder.appendLine("\n### Target FPS Ranges\n`${fpsRanges?.contentToString()}`")

            val formats = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)?.outputFormats?.joinToString()
            builder.appendLine("\n### Supported Output Formats\n`${formats}`")

            val capabilities = characteristics.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES)
            val supportsLogicalMultiCamera = capabilities?.contains(
                CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_LOGICAL_MULTI_CAMERA
            ) ?: false
            builder.appendLine("\n### Multi-frame HDR Support\nLogical Multi-Camera: `$supportsLogicalMultiCamera`")

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                val recommended10Bit = characteristics.get(CameraCharacteristics.REQUEST_RECOMMENDED_TEN_BIT_DYNAMIC_RANGE_PROFILE)
                builder.appendLine("\n### 10-bit HDR Profile\n${recommended10Bit ?: "Unavailable"}")
            }
        }

        // Memory Info
        val memoryInfo = ActivityManager.MemoryInfo()
        val activityManager = getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        activityManager.getMemoryInfo(memoryInfo)

        builder.appendLine("\n## Memory Info")
        builder.appendLine("- Available Mem: ${memoryInfo.availMem / 1048576L} MB")
        builder.appendLine("- Total Mem: ${memoryInfo.totalMem / 1048576L} MB")
        builder.appendLine("- Low Mem? ${memoryInfo.lowMemory}")

        val pid = android.os.Process.myPid()
        val memStats = activityManager.getProcessMemoryInfo(intArrayOf(pid))[0]
        builder.appendLine("- Dalvik: ${memStats.dalvikPrivateDirty} KB")
        builder.appendLine("- Native: ${memStats.nativePrivateDirty} KB")
        builder.appendLine("- Total PSS: ${memStats.totalPss} KB")

        builder.appendLine("\n_Generated on ${LocalDateTime.now()}_")

        // Save to file
        contentResolver.openOutputStream(uri)?.use { outputStream ->
            outputStream.write(builder.toString().toByteArray())
        } ?: run {
            Toast.makeText(this, "Unable to write to file", Toast.LENGTH_SHORT).show()
        }
    }
}


