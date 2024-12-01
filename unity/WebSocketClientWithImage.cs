using System.Collections;
using System.Threading.Tasks;
using UnityEngine;
using WebSocketSharp;

public class WebSocketClientWithImage : MonoBehaviour
{
    private WebSocket _webSocket;
    private const string WEBSOCKET_URL = "wss://648e-220-96-82-1.ngrok-free.app";

    [SerializeField] private Camera targetCamera;
    private bool _isSendingImages = true; // 送信中フラグ
    private Texture2D _capturedImage; // キャプチャ済みの画像を一時保存

    private void Start()
    {
        // WebSocket初期化
        _webSocket = new WebSocket(WEBSOCKET_URL);

        // SSL証明書の検証を無効化（開発用のみ）
        _webSocket.SslConfiguration.ServerCertificateValidationCallback += (sender, certificate, chain, sslPolicyErrors) => true;

        // イベント登録
        _webSocket.OnOpen += (sender, e) => Debug.Log("WebSocket connected.");
        _webSocket.OnMessage += (sender, e) => Debug.Log($"Received: {e.Data}");
        _webSocket.OnError += (sender, e) => Debug.LogError($"WebSocket Error: {e.Message}");
        _webSocket.OnClose += (sender, e) => HandleWebSocketClosure();

        // 接続
        ConnectWebSocket();

        // targetCamera が未割り当てなら、自動で Main Camera を取得
        if (targetCamera == null)
        {
            targetCamera = Camera.main;
            if (targetCamera == null)
            {
                Debug.LogError("No camera found. Please assign a camera to 'targetCamera' in the inspector.");
                return; // カメラがない場合は処理を中断
            }
        }

        targetCamera.aspect = 16.0f / 9.0f;

        // 非同期で画像送信を開始
        Debug.Log("Starting asynchronous image sending...");
        StartCoroutine(CaptureAndSendImages());
    }

    private void ConnectWebSocket()
    {
        _webSocket.Connect();
        if (!_webSocket.IsAlive)
        {
            Debug.LogWarning("Failed to connect WebSocket. Retrying...");
            StartCoroutine(RetryConnection());
        }
    }

    private IEnumerator RetryConnection()
    {
        while (!_webSocket.IsAlive)
        {
            Debug.Log("Retrying WebSocket connection...");
            _webSocket.Connect();
            yield return new WaitForSeconds(2); // 2秒後に再接続を試みる
        }

        Debug.Log("WebSocket reconnected.");
    }

    private void HandleWebSocketClosure()
    {
        Debug.LogWarning("WebSocket closed. Attempting to reconnect...");
        StartCoroutine(RetryConnection());
    }

    private IEnumerator CaptureAndSendImages()
    {
        while (_isSendingImages)
        {
            // メインスレッドでカメラ画像をキャプチャ
            yield return new WaitForEndOfFrame();

            _capturedImage = CaptureCameraImage(targetCamera);

            // 非同期で画像データを送信
            if (_capturedImage != null)
            {
                byte[] imageData = _capturedImage.EncodeToJPG(75); // JPG圧縮率を調整
                Task.Run(() => SendImageData(imageData));

                Destroy(_capturedImage); // メモリ解放
            }

            // 次のフレームまで待機
            yield return new WaitForSeconds(0.1f); // 送信間隔を調整（50msごとに送信）
        }
    }

    private void SendImageData(byte[] imageData)
    {
        if (_webSocket != null && _webSocket.IsAlive)
        {
            _webSocket.Send(imageData);
            Debug.Log($"Image sent: {imageData.Length} bytes at {System.DateTime.Now}");
        }
        else
        {
            Debug.LogWarning("WebSocket is not connected.");
        }
    }

    private Texture2D CaptureCameraImage(Camera camera)
    {
        int width = 1280; // 解像度を低く設定
        int height = 720;

        RenderTexture renderTexture = new RenderTexture(width, height, 24);
        camera.targetTexture = renderTexture;
        camera.Render();
        RenderTexture.active = renderTexture;

        Texture2D texture = new Texture2D(width, height, TextureFormat.RGB24, false);
        texture.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        texture.Apply();

        camera.targetTexture = null;
        RenderTexture.active = null;
        Destroy(renderTexture);

        return texture;
    }

    private void OnDestroy()
    {
        if (_webSocket != null)
        {
            _isSendingImages = false; // 非同期ループを停止
            _webSocket.Close();
            _webSocket = null;
        }
    }
}

